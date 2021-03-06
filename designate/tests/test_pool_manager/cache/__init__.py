# Copyright 2014 eBay Inc.
#
# Author: Ron Rickard <rrickard@ebaysf.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import testtools

from designate import exceptions
from designate import objects
from designate.pool_manager.cache.base import PoolManagerCache


class PoolManagerCacheTestCase(object):
    def create_pool_manager_status(self):
        values = {
            'server_id': '896aa661-198c-4379-bccd-5d8de7007030',
            'domain_id': 'bce45113-4a22-418d-a54d-c9777d056312',
            'action': 'CREATE',
            'status': 'SUCCESS',
            'serial_number': 1
        }
        return objects.PoolManagerStatus(**values)

    def test_interface(self):
        self._ensure_interface(PoolManagerCache, self.cache.__class__)

    def test_store_and_clear_and_retrieve(self):
        expected = self.create_pool_manager_status()
        self.cache.store(self.admin_context, expected)

        self.cache.clear(self.admin_context, expected)

        with testtools.ExpectedException(exceptions.PoolManagerStatusNotFound):
            self.cache.retrieve(
                self.admin_context, expected.server_id, expected.domain_id,
                expected.action)

    def test_retrieve(self):
        expected = self.create_pool_manager_status()
        with testtools.ExpectedException(exceptions.PoolManagerStatusNotFound):
            self.cache.retrieve(
                self.admin_context, expected.server_id, expected.domain_id,
                expected.action)
