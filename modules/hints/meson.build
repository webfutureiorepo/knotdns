# C module: hints
# SPDX-License-Identifier: GPL-3.0-or-later

hints_src = files([
  'hints.c',
])
c_src_lint += hints_src

hints_mod = shared_module(
  'hints',
  hints_src,
  dependencies: mod_deps,
  include_directories: mod_inc_dir,
  name_prefix: '',
  install: true,
  install_dir: modules_dir,
  link_with: kresd,
)

config_tests += [
  ['hints', files('tests/hints.test.lua')],
]
