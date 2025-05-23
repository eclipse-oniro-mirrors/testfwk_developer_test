#!/usr/bin/env python3
# coding=utf-8

#
# Copyright (c) 2022 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
from main import Console
from xdevice import platform_logger
try:
    from xdevice.__main__ import check_report_template
    is_check_report_template = True
except ImportError:
    is_check_report_template = False



LOG = platform_logger("main")


def main_process():
    LOG.info("************* Developer Test Framework Starting **************")
    console = Console()
    if is_check_report_template:
        check_report_template()
    console.console(sys.argv)
    LOG.info("************* Developer Test Framework Finished **************")


if __name__ == "__main__":
    main_process()
