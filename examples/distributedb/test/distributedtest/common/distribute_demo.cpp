/*
 * Copyright (c) 2021 Huawei Device Co., Ltd.
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

#include <iostream>

#include "distributed_major.h"

#include "refbase.h"
#include "hilog/log.h"

using namespace std;
using namespace OHOS;
using namespace testing::ext;
using namespace OHOS::DistributeSystemTest;
using namespace OHOS::HiviewDFX;

namespace
{
    constexpr HiLogLabel LABEL={LOG_CORE,0,"DistributedtestDemo"};
	// const int SYNC_REC_TIME = 3;

    const int MSG_LENGTH = 100;
    const int EXPECT_RETURN_VALUE = 111;
}

class DistributedtestDemo:public DistributeTest{
public:
    DistributedtestDemo() = default;
    ~DistributedtestDemo() = default;

    static void SetUpTestCase();
    static void TearDownTestCase();
    virtual void SetUp();
    virtual void TearDown();
};

void DistributedtestDemo::SetUpTestCase()
{

}

void DistributedtestDemo::TearDownTestCase()
{

}

void DistributedtestDemo::SetUp()
{

}

void DistributedtestDemo::TearDown()
{

}

/*
* @tc.name:SendMessageTest001
* @tc.desc:Verify the distributed test framework interface SendMessage.
* @tc.type:FUNC
* @tc.require:ArOOOCQGMV
*/
HWTEST_F(DistributedtestDemo, SendMessageTest001,TestSize.Level1)
{
    char msgbuf[MSG_LENGTH] = "I am testcase 1";
    int ret = SendMessage(AGENT_NO::ONE,msgbuf,MSG_LENGTH);

	// EXPECT_TRUE(ret)<<"ret = 0";
    if(ret == 0)
    {
        EXPECT_FALSE(ret)<<"ret = 2";
	}

}

HWTEST_F(DistributedtestDemo, SendMessageTest002, TestSize.Level1)
{
    char msgbuf[MSG_LENGTH] = "I am recall";
    int ret = SendMessage(AGENT_NO::ONE, msgbuf,MSG_LENGTH,[&](const std::string &szreturnbuf, int rlen)->bool{
        std::string szbuf = "ok";
		// EXPECT_TRUE(szbuf == szreturnbuf)<<"字符串是相等的";
        HiLog::Info(LABEL, "SendMessageTest002 = %s",szbuf.c_str());
        return true;
	});

    if(ret == 0)
    {
        EXPECT_TRUE(1)<<"ret = 0";
    }
}

HWTEST_F(DistributedtestDemo, SendMessageTest003, TestSize.Level1)
{
    char msgbuf[MSG_LENGTH] = "I am testcase 2";
	    int ret = SendMessage(AGENT_NO::ONE, msgbuf, MSG_LENGTH);
    if(ret == 0)
    {
        EXPECT_FALSE(ret)<<"ret = 0";
    }

}


HWTEST_F(DistributedtestDemo, RunCmdOnAgent001, TestSize.Level1)
{
    std::string command = "query_command";
    std::string cmdArgs = "query a name?";
    std::string expectValue = "111";
    RunCmdOnAgent(AGENT_NO::ONE, command, cmdArgs, expectValue);
    EXPECT_EQ(GetReturnVal(), EXPECT_RETURN_VALUE);
}

int main(int argc, char*argv[])
{
    g_pDistributetestEnv = new DistributeTestEnvironment("major.desc");
    testing::AddGlobalTestEnvironment(g_pDistributetestEnv);
    testing::GTEST_FLAG(output) = "xml:./";
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}