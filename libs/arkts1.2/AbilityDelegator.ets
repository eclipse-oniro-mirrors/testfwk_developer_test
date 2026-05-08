/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { BusinessError } from '@ohos.base';
import { ShellCmdResult } from 'ShellCmdResult'
import AbilityMonitor from 'AbilityMonitor';
import AbilityStageMonitor from 'AbilityStageMonitor';
import UIAbility from '@ohos.app.ability.UIAbility';
import AbilityStage from '@ohos.app.ability.AbilityStage';
import Want from '@ohos.app.ability.Want';

type AsyncCallback<T, E = void> = (error: BusinessError<E>, data: T) => void;

export interface AbilityDelegator {

  printSync(msg: string): void;

  finishTest(msg: string, code: long, callback: AsyncCallback<void>): void;

  finishTest(msg: string, code: long): Promise<void>;

  executeShellCommand(cmd: String, callback: AsyncCallback<ShellCmdResult>): void;

  executeShellCommand(cmd: String, timeoutSecs: long, callback: AsyncCallback<ShellCmdResult>): void;

  executeShellCommand(cmd: string, timeoutSecs?: long): Promise<ShellCmdResult>;

  addAbilityMonitor(monitor: AbilityMonitor, callback: AsyncCallback<void>): void;

  addAbilityMonitor(monitor: AbilityMonitor): Promise<void>;

  removeAbilityMonitor(monitor: AbilityMonitor, callback: AsyncCallback<void>): void;

  removeAbilityMonitor(monitor: AbilityMonitor): Promise<void>;

  waitAbilityMonitor(monitor: AbilityMonitor, callback: AsyncCallback<UIAbility>): void;

  waitAbilityMonitor(monitor: AbilityMonitor, timeout: long, callback: AsyncCallback<UIAbility>): void;

  waitAbilityMonitor(monitor: AbilityMonitor, timeout?: long): Promise<UIAbility>;

  addAbilityStageMonitor(monitor: AbilityStageMonitor, callback: AsyncCallback<void>): void;

  addAbilityStageMonitor(monitor: AbilityStageMonitor): Promise<void>;

  removeAbilityStageMonitor(monitor: AbilityStageMonitor, callback: AsyncCallback<void>): void;

  removeAbilityStageMonitor(monitor: AbilityStageMonitor): Promise<void>;

  waitAbilityStageMonitor(monitor: AbilityStageMonitor, callback: AsyncCallback<AbilityStage>): void;

  waitAbilityStageMonitor(monitor: AbilityStageMonitor, timeout: long, callback: AsyncCallback<AbilityStage>): void;

  waitAbilityStageMonitor(monitor: AbilityStageMonitor, timeout?: long): Promise<AbilityStage>;

  doAbilityForeground(ability: UIAbility, callback: AsyncCallback<void>): void;

  doAbilityForeground(ability: UIAbility): Promise<void>;

  doAbilityBackground(ability: UIAbility, callback: AsyncCallback<void>): void;

  doAbilityBackground(ability: UIAbility): Promise<void>;

  print(msg: string, callback: AsyncCallback<void>): void;

  print(msg: string): Promise<void>;

  startAbility(want: Want, callback: AsyncCallback<void>): void;

  startAbility(want: Want): Promise<void>;

  getCurrentTopAbility(callback: AsyncCallback<UIAbility>): void;

  getCurrentTopAbility(): Promise<UIAbility>;
}

export class AbilityDelegatorInner implements AbilityDelegator {

  printSync(msg: string): void {};

  finishTest(msg: string, code: long, callback: AsyncCallback<void>): void {};

  finishTest(msg: string, code: long): Promise<void> {
    return new Promise<void>((resolve: (data: undefined) => void, reject: (err: BusinessError) => void): void => {
    });
  }

  executeShellCommand(cmd: String, callback: AsyncCallback<ShellCmdResult, void>): void{};

  executeShellCommand(cmd: string, timeoutSecs: long, callback: AsyncCallback<ShellCmdResult, void>): void {};

  executeShellCommand(cmd: string, timeoutSecs?: long): Promise<ShellCmdResult> {
    return new Promise<ShellCmdResult>((resolve: (data: ShellCmdResult) => void,
      reject: (err: BusinessError) => void): void => {
    });
  }

  addAbilityMonitor(monitor: AbilityMonitor, callback: AsyncCallback<void>): void {};

  addAbilityMonitor(monitor: AbilityMonitor): Promise<void> {
    return new Promise<void>((resolve: (data: undefined) => void, reject: (err: BusinessError) => void): void => {
    });
  }

  removeAbilityMonitor(monitor: AbilityMonitor, callback: AsyncCallback<void>): void {};

  removeAbilityMonitor(monitor: AbilityMonitor): Promise<void> {
    return new Promise<void>((resolve: (data: undefined) => void, reject: (err: BusinessError) => void): void => {
    });
  }

  waitAbilityMonitor(monitor: AbilityMonitor, callback: AsyncCallback<UIAbility, void>): void {};

  waitAbilityMonitor(monitor: AbilityMonitor, timeout: long, callback: AsyncCallback<UIAbility, void>): void {};

  waitAbilityMonitor(monitor: AbilityMonitor, timeout?: long): Promise<UIAbility> {
    return new Promise<UIAbility>((resolve: (data: UIAbility) => void, reject: (err: BusinessError) => void): void => {
    });
  }

  addAbilityStageMonitor(monitor: AbilityStageMonitor, callback: AsyncCallback<void>): void {};

  addAbilityStageMonitor(monitor: AbilityStageMonitor): Promise<void> {
    return new Promise<void>((resolve: (data: undefined) => void, reject: (err: BusinessError) => void): void => {
    });
  }

  removeAbilityStageMonitor(monitor: AbilityStageMonitor, callback: AsyncCallback<void>): void {};

  removeAbilityStageMonitor(monitor: AbilityStageMonitor): Promise<void> {
    return new Promise<void>((resolve: (data: undefined) => void, reject: (err: BusinessError) => void): void => {
    });
  }

  waitAbilityStageMonitor(monitor: AbilityStageMonitor, callback: AsyncCallback<AbilityStage, void>): void {};

  waitAbilityStageMonitor(monitor: AbilityStageMonitor, timeout: long,
    callback: AsyncCallback<AbilityStage, void>): void {};

  waitAbilityStageMonitor(monitor: AbilityStageMonitor, timeout?: long): Promise<AbilityStage> {
    return new Promise<AbilityStage>((resolve: (data: AbilityStage) => void,
      reject: (err: BusinessError) => void): void => {
    });
  }

  doAbilityForeground(ability: UIAbility, callback: AsyncCallback<void>): void {};

  doAbilityForeground(ability: UIAbility): Promise<void> {
    return new Promise<void>((resolve: (data: undefined) => void, reject: (err: BusinessError) => void): void => {
    });
  }

  doAbilityBackground(ability: UIAbility, callback: AsyncCallback<void>): void {};

  doAbilityBackground(ability: UIAbility): Promise<void> {
    return new Promise<void>((resolve: (data: undefined) => void, reject: (err: BusinessError) => void): void => {
    });
  }

  print(msg: string, callback: AsyncCallback<void>): void {};

  print(msg: string): Promise<void> {
    return new Promise<void>((resolve: (data: undefined) => void, reject: (err: BusinessError) => void): void => {
    });
  }

  startAbility(want: Want, callback: AsyncCallback<void>): void {};

  startAbility(want: Want): Promise<void> {
    return new Promise<void>((resolve: (data: undefined) => void, reject: (err: BusinessError) => void): void => {
    });
  }

  getCurrentTopAbility(callback: AsyncCallback<UIAbility, void>): void {};

  getCurrentTopAbility(): Promise<UIAbility> {
    return new Promise<UIAbility>((resolve: (v: UIAbility) => void, reject: (error: Error) => void) => {
    });
  }
}