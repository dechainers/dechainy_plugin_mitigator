# Copyright 2022 DeChainers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import unittest

from dechainy.controller import Controller

controller = Controller()


@unittest.skipIf(os.getuid(), reason='Root for BCC')
class TestMitigator(unittest.TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        controller.delete_probe(plugin_name='mitigator')
        controller.delete_plugin('mitigator')

    def test1_add_plugin(self):
        controller.create_plugin(os.path.join(os.path.dirname(
            __file__), os.pardir, "mitigator"), update=True)

    def test2_create_probe(self):
        controller.create_probe('mitigator', 'attempt', interface='lo')

    def test3_insert_rule(self):
        rule = controller.get_plugin('mitigator').MitigatorRule('8.8.8.8', 32)
        p = controller.get_probe('mitigator', 'attempt')
        p.insert(rule)
        assert len(p.get()) == 1

    def test4_insert_error(self):
        rule = controller.get_plugin('mitigator').MitigatorRule('8.8.8.8', 32)
        p = controller.get_probe('mitigator', 'attempt')
        with self.assertRaises(LookupError):
            p.insert(rule)

    def test5_delete_rule(self):
        rule = controller.get_plugin('mitigator').MitigatorRule('8.8.8.8', 32)
        p = controller.get_probe('mitigator', 'attempt')
        p.delete(rule)
        assert len(p.get()) == 0

    def test6_insert_at_error(self):
        rule = controller.get_plugin('mitigator').MitigatorRule('8.8.8.8', 32)
        p = controller.get_probe('mitigator', 'attempt')
        with self.assertRaises(IndexError):
            p.insert_at(10, rule)


if __name__ == '__main__':
    unittest.main()
