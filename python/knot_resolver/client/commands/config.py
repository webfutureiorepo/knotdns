import argparse
import sys
from enum import Enum
from typing import List, Literal, Optional, Tuple, Type

from knot_resolver.client.command import COMP_NOSPACE, Command, CommandArgs, CompWords, comp_get_words, register_command
from knot_resolver.datamodel import KresConfig
from knot_resolver.utils.modeling.parsing import DataFormat, parse_json, try_to_parse
from knot_resolver.utils.requests import request


class Operations(Enum):
    SET = 0
    DELETE = 1
    GET = 2


def operation_to_method(operation: Operations) -> Literal["PUT", "GET", "DELETE"]:
    if operation == Operations.SET:
        return "PUT"
    if operation == Operations.DELETE:
        return "DELETE"
    return "GET"


@register_command
class ConfigCommand(Command):
    def __init__(self, namespace: argparse.Namespace) -> None:
        super().__init__(namespace)
        self.path: str = str(namespace.path) if hasattr(namespace, "path") else ""
        self.format: DataFormat = namespace.format if hasattr(namespace, "format") else DataFormat.JSON
        self.operation: Optional[Operations] = namespace.operation if hasattr(namespace, "operation") else None
        self.file: Optional[str] = namespace.file if hasattr(namespace, "file") else None

    @staticmethod
    def register_args_subparser(
        subparser: "argparse._SubParsersAction[argparse.ArgumentParser]",
    ) -> Tuple[argparse.ArgumentParser, "Type[Command]"]:
        config = subparser.add_parser("config", help="Performs operations on the running resolver's configuration.")
        path_help = "Optional, path (JSON pointer, RFC6901) to the configuration resources. By default, the entire configuration is selected."

        config_subparsers = config.add_subparsers(help="operation type")

        # GET operation
        get_op = config_subparsers.add_parser("get", help="Get current configuration from the resolver.")
        get_op.set_defaults(operation=Operations.GET, format=DataFormat.YAML)

        get_op.add_argument(
            "-p",
            "--path",
            help=path_help,
            action="store",
            type=str,
            default="",
        )
        get_op.add_argument(
            "file",
            help="Optional, path to the file where to save exported configuration data. If not specified, data will be printed.",
            type=str,
            nargs="?",
        )

        get_formats = get_op.add_mutually_exclusive_group()
        get_formats.add_argument(
            "--json",
            help="Get configuration data in JSON format.",
            const=DataFormat.JSON,
            action="store_const",
            dest="format",
        )
        get_formats.add_argument(
            "--yaml",
            help="Get configuration data in YAML format, default.",
            const=DataFormat.YAML,
            action="store_const",
            dest="format",
        )

        # SET operation
        set_op = config_subparsers.add_parser("set", help="Set new configuration for the resolver.")
        set_op.set_defaults(operation=Operations.SET)

        set_op.add_argument(
            "-p",
            "--path",
            help=path_help,
            action="store",
            type=str,
            default="",
        )

        value_or_file = set_op.add_mutually_exclusive_group()
        value_or_file.add_argument(
            "file",
            help="Optional, path to file with new configuration.",
            type=str,
            nargs="?",
        )
        value_or_file.add_argument(
            "value",
            help="Optional, new configuration value.",
            type=str,
            nargs="?",
        )

        # DELETE operation
        delete_op = config_subparsers.add_parser(
            "delete", help="Delete given configuration property or list item at the given index."
        )
        delete_op.set_defaults(operation=Operations.DELETE)
        delete_op.add_argument(
            "-p",
            "--path",
            help=path_help,
            action="store",
            type=str,
            default="",
        )
        return config, ConfigCommand

    @staticmethod
    def completion(args: List[str], parser: argparse.ArgumentParser) -> CompWords:
        nargs = len(args)

        if nargs > 1 and args[-2] in ["-p", "--path"]:
            words: CompWords = {}
            words[COMP_NOSPACE] = None

            path = args[-1]
            path_nodes = path.split("/")

            prefix = ""
            properties = KresConfig.json_schema()["properties"]
            is_list = False
            for i, node in enumerate(path_nodes):
                # first node is empty string
                if i == 0:
                    continue

                if node in properties:
                    is_list = False
                    if "properties" in properties[node]:
                        properties = properties[node]["properties"]
                        prefix += f"/{node}"
                        continue
                    if "items" in properties[node]:
                        properties = properties[node]["items"]["properties"]
                        prefix += f"/{node}"
                        is_list = True
                        continue
                    del words[COMP_NOSPACE]
                    break
                if is_list and node.isnumeric():
                    prefix += f"/{node}"
                    continue

            for key in properties.keys():
                words[f"{prefix}/{key}"] = properties[key]["description"]

            return words

        return comp_get_words(args, parser)

    def run(self, args: CommandArgs) -> None:
        if not self.operation:
            args.subparser.print_help()
            sys.exit()

        new_config = None
        path = f"v1/config{self.path}"
        method = operation_to_method(self.operation)

        if self.operation == Operations.SET:
            if self.file:
                try:
                    with open(self.file, "r") as f:
                        new_config = f.read()
                except FileNotFoundError:
                    new_config = self.file
            else:
                # use STDIN also when file is not specified
                new_config = input("Type new configuration: ")

        body = DataFormat.JSON.dict_dump(try_to_parse(new_config)) if new_config else None
        response = request(args.socket, method, path, body)

        if response.status != 200:
            print(response, file=sys.stderr)
            sys.exit(1)

        if self.operation == Operations.GET and self.file:
            with open(self.file, "w") as f:
                f.write(self.format.dict_dump(parse_json(response.body), indent=4))
            print(f"saved to: {self.file}")
        elif response.body:
            print(self.format.dict_dump(parse_json(response.body), indent=4))
