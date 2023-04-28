from copy import deepcopy
import io
import json
import pathlib
from typing import Any, List
from datetime import datetime

import pytest
from pytest_mock import MockerFixture
from xgnlog.Log import Level

from src.abc_process import Mode, ProcessStatus
import src.xcap_tool as target

JOB_ID = "T23AJ001"


def get_1st_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("1st_xcap_tool.log")


def get_2nd_log_path(tmpdir: str) -> pathlib.Path:
    return pathlib.Path(tmpdir).joinpath("2nd_xcap_tool.log")


DICT_TOOL = {
    "nf_infos": "nf-infos.json",
    "edns_infos": "edns-infos.json"
}
DICT_SMFV = {
    "a2-er-s01-smfvoroout-001": {
        "xCAP": [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    },
    "b1-er-s01-smfvoroout-001": {
        "xCAP": [
            "2001:268:200d:1010::6",
            "2001:268:200d:5010::6",
            "2001:268:200d:500f::6"
        ]
    }
}
DICT_EDNS = {
    "tys1tb1edns02": {
        "ipaddr": "2001:268:200d:1010::6"
    },
    "tys1tb2edns02": {
        "ipaddr": "2001:268:200d:5010::6"
    },
    "tys1tb3edns02": {
        "ipaddr": "2001:268:200d:500f::6"
    }
}


class MockLog():
    def __init__(self, job_id: str, init_level: Level, log_dir: str) -> None:
        self.job_id = job_id
        self.init_level = init_level
        self.log_path_1st = get_1st_log_path(log_dir)
        self.log_path_2nd = get_2nd_log_path(log_dir)

    def output_1st_log(self, msg_id: str, add_info: Any = None) -> None:
        with open(self.log_path_1st, "a", encoding="utf-8", newline="\n") as f:
            f.write("job_id:{0}, message_id:{1}, add_info:{2}\n".format(self.job_id, msg_id, add_info))

    def output_2nd_log(self, level: Level, add_info: Any = None) -> None:
        with open(self.log_path_2nd, "a", encoding="utf-8", newline="\n") as f:
            f.write("job_id:{0}, level:{1}, add_info:{2}\n".format(self.job_id, level.name, add_info))


class MockProcess:
    def __init__(self,
                 edns_name: str,
                 nf_name: str,
                 mode: Mode,
                 edns_ipaddr: str,
                 ipaddr_list: List[str],
                 stub: bool,
                 job_id: str):
        pass

    def run(self):
        pass


def test_ToolResult01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """ToolResult試験01 Enum取得

    試験条件
    ・status = ToolResult.ok
    ・value = "OK"

    試験結果
    ・値が取得できること
    ・標準出力がないこと
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    status = target.ToolResult.ok
    value = target.ToolResult.ok.value

    expected_value = value

    expected_log_1st = []

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)

    response_value = str(status)

    assert response_value == expected_value


def test_check_args01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """check_args試験01 正常試験 (mode: LIST, node: なし)

    試験条件
    ・コマンド引数
        ・script_name = "xcap_tool.py"
        ・mode = Mode.list

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "xcap_tool.py"
    mode = Mode.list
    blocked_nf = ""
    batch = False
    stub = False
    argv = [script_name, mode.value]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00103, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00104, add_info:{[target.NF_NONE] + argv[1:]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.XcapTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.edns_name is not None
    assert tool.args.edns_name == target.NF_NONE
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """check_args試験02 正常試験 (mode: LIST, node: あり)

    試験条件
    ・コマンド引数
        ・script_name = "xcap_tool.py"
        ・edns_name = "tys1tb1edns02"
        ・mode = Mode.list
        ・blocked_node = ""
        ・batch = False
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "xcap_tool.py"
    edns_name = "tys1tb1edns02"
    mode = Mode.list
    blocked_nf = ""
    batch = False
    stub = False
    argv = [script_name, edns_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00103, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00104, add_info:{argv[1:]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.XcapTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.edns_name is not None
    assert tool.args.edns_name == edns_name
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """check_args試験03 正常試験 (mode: INFO)

    試験条件
    ・コマンド引数
        ・script_name = "xcap_tool.py"
        ・edns_name = "tys1tb1edns02"
        ・mode = Mode.info
        ・blocked_node = ""
        ・batch = False
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "xcap_tool.py"
    edns_name = "tys1tb1edns02"
    mode = Mode.info
    blocked_nf = ""
    batch = False
    stub = False
    argv = [script_name, edns_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00103, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00104, add_info:{argv[1:]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.XcapTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.edns_name is not None
    assert tool.args.edns_name == edns_name
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """check_args試験04 正常試験 (mode: SHOW)

    試験条件
    ・コマンド引数
        ・script_name = "xcap_tool.py"
        ・edns_name = "tys1tb1edns02"
        ・mode = Mode.show
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = False
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "xcap_tool.py"
    edns_name = "tys1tb1edns02"
    mode = Mode.show
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = False
    stub = False
    argv = [script_name, edns_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00103, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00104, add_info:{argv[1:]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.XcapTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.edns_name is not None
    assert tool.args.edns_name == edns_name
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """check_args試験05 準正常試験 (mode: UP)

    試験条件
    ・コマンド引数
        ・script_name = "xcap_tool.py"
        ・edns_name = "tys1tb1edns02"
        ・mode = Mode.up
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = False
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    script_name = "xcap_tool.py"
    edns_name = "tys1tb1edns02"
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = False
    stub = False
    argv = [script_name, edns_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{target.MODE_UNKNOWN}:{logtime_str}:{target.NF_NONE}({target.NF_NONE}):failed to analyse arguments {argv[1:]}.\n",
        f"[RESULT]:{target.MODE_UNKNOWN}:{logtime_str}:{target.NF_NONE}({target.NF_NONE}):[ {tool_expected_value} ]\n",
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00103, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:E00102, add_info:{argv[1:]}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:引数解析異常発生:\n",
        "パラメータ:\n",
        f" 引数: {argv[1:]}\n",
        " Trace: ArgumentParserError argument mode: invalid choice: <Mode.up: 'UP'> (choose from <Mode.down: 'DOWN'>, <Mode.show: 'SHOW'>, <Mode.info: 'INFO'>, <Mode.list: 'LIST'>)\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert not hasattr(tool, "args")
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_check_args06(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """check_args試験06 正常試験 (mode: DOWN)

    試験条件
    ・コマンド引数
        ・script_name = "xcap_tool.py"
        ・edns_name = "tys1tb1edns02"
        ・mode = Mode.down
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = False
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "xcap_tool.py"
    edns_name = "tys1tb1edns02"
    mode = Mode.down
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = False
    stub = False
    argv = [script_name, edns_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00103, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00104, add_info:{argv[1:]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.XcapTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.edns_name is not None
    assert tool.args.edns_name == edns_name
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args07(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """check_args試験07 準正常試験 (mode: UP, batch: True)

    試験条件
    ・コマンド引数
        ・script_name = "xcap_tool.py"
        ・edns_name = "tys1tb1edns02"
        ・mode = Mode.up
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = True
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がNoneであること
    ・各コマンド引数が正常に取得できること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    script_name = "xcap_tool.py"
    edns_name = "tys1tb1edns02"
    mode = Mode.up
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = True
    stub = False
    argv = [script_name, edns_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{target.MODE_UNKNOWN}:{logtime_str}:{target.NF_NONE}({target.NF_NONE}):failed to analyse arguments {argv[1:]}.\n",
        f"[RESULT]:{target.MODE_UNKNOWN}:{logtime_str}:{target.NF_NONE}({target.NF_NONE}):[ {tool_expected_value} ]\n",
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00103, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:E00102, add_info:{argv[1:]}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:引数解析異常発生:\n",
        "パラメータ:\n",
        f" 引数: {argv[1:]}\n",
        " Trace: ArgumentParserError argument mode: invalid choice: <Mode.up: 'UP'> (choose from <Mode.down: 'DOWN'>, <Mode.show: 'SHOW'>, <Mode.info: 'INFO'>, <Mode.list: 'LIST'>)\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert not hasattr(tool, "args")
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_check_args08(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """check_args試験08 正常試験 (mode: DOWN, stub:True)

    試験条件
    ・コマンド引数
        ・script_name = "xcap_tool.py"
        ・edns_name = "tys1tb1edns02"
        ・mode = Mode.down
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = False
        ・stub = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・各コマンド引数が正常に取得できること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "xcap_tool.py"
    edns_name = "tys1tb1edns02"
    mode = Mode.down
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = False
    stub = True
    argv = [script_name, edns_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = True

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00103, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00104, add_info:{argv[1:]}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    tool = target.XcapTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert tool.args.edns_name is not None
    assert tool.args.edns_name == edns_name
    assert tool.args.mode is not None
    assert tool.args.mode == mode
    assert tool.args.blocked_nflist is not None
    assert tool.args.blocked_nflist == blocked_nflist
    assert tool.args.batch is not None
    assert tool.args.batch == batch
    assert tool.args.stub is not None
    assert tool.args.stub == stub
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_check_args09(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """check_args試験09 異常系試験 (edns_name: なし)

    試験条件
    ・コマンド引数
        ・script_name = "xcap_tool.py"
        ・edns_name = ""
        ・mode = Mode.down
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = False
        ・stub = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    script_name = "xcap_tool.py"
    edns_name = ""
    mode = Mode.show
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = False
    stub = False
    argv = [script_name, edns_name, mode.value, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{target.MODE_UNKNOWN}:{logtime_str}:{target.NF_NONE}({target.NF_NONE}):failed to analyse arguments {argv[1:]}.\n",
        f"[RESULT]:{target.MODE_UNKNOWN}:{logtime_str}:{target.NF_NONE}({target.NF_NONE}):[ {tool_expected_value} ]\n",
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00103, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:E00102, add_info:{argv[1:]}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:引数解析異常発生:\n",
        "パラメータ:\n",
        f" 引数: {argv[1:]}\n",
        " Trace: ArgumentParserError Argument is None, null string or blank only.\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_check_args10(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """check_args試験10 異常系試験 (mode: なし)

    試験条件
    ・コマンド引数
        ・script_name = "xcap_tool.py"
        ・edns_name = "tys1tb1edns02"
        ・mode = ""
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = False
        ・stub = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseとなること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    script_name = "xcap_tool.py"
    edns_name = "tys1tb1edns02"
    mode = ""
    blocked_nf = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
    batch = False
    stub = False
    argv = [script_name, edns_name, mode, blocked_nf]
    blocked_nflist = blocked_nf.split(",")
    if batch:
        argv.append("--batch")
    if stub:
        argv.append("--stub")
    if "" in blocked_nflist:
        blocked_nflist.remove("")

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{target.MODE_UNKNOWN}:{logtime_str}:{target.NF_NONE}({target.NF_NONE}):failed to analyse arguments {argv[1:]}.\n",
        f"[RESULT]:{target.MODE_UNKNOWN}:{logtime_str}:{target.NF_NONE}({target.NF_NONE}):[ {tool_expected_value} ]\n",
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00103, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:E00102, add_info:{argv[1:]}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:引数解析異常発生:\n",
        "パラメータ:\n",
        f" 引数: {argv[1:]}\n",
        " Trace: ArgumentParserError argument mode: invalid Mode value: ''\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)
    mocker.patch("sys.argv", new=argv)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    response_value = tool.check_args()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_load_config01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """load_config試験01 正常系試験

    試験条件
    ・全設定ファイルを指定

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・json_check_and_loadが3回呼ばれること
    ・tool_confが想定しているdictであること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down

    tool_dict_expected_value = {
        "nf_infos": DICT_SMFV,
        "edns_infos": DICT_EDNS
    }

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00105, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00106, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.load = mocker.Mock(side_effect=[deepcopy(DICT_TOOL), deepcopy(DICT_SMFV), deepcopy(DICT_EDNS)])
    mocker.patch("src.xcap_tool.json.load", test_mocker.load)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.load_config()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.load.called == True
    assert test_mocker.load.call_count == 3
    assert tool.tool_conf == tool_dict_expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_load_config02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """load_config試験02 異常系試験 (ファイルなし)

    試験条件
    ・全設定ファイルを指定
    ・FileNotFoundError発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseであること
    ・json_check_and_loadが4回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down

    edns_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "edns-infos.json")

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({target.NF_NONE}):configuration files not found. file={edns_conf_path}\n",
        f"[RESULT]:{mode}:{logtime_str}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00105, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:E00103, add_info:{edns_conf_path}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:設定ファイルなし発生:\n",
        "パラメータ:\n",
        f" ファイルパス: {edns_conf_path}\n",
        f" Trace: FileNotFoundError File Not Found\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.load = mocker.Mock(side_effect=[deepcopy(DICT_TOOL), deepcopy(DICT_SMFV), FileNotFoundError("File Not Found")])
    mocker.patch("src.xcap_tool.json.load", test_mocker.load)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.load_config()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.load.called == True
    assert test_mocker.load.call_count == 3
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_load_config03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """load_config試験03 異常系試験 (JSON解析エラー)

    試験条件
    ・全設定ファイルを指定
    ・JSONDecodeError発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseであること
    ・json_check_and_loadが4回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down

    edns_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "edns-infos.json")

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({target.NF_NONE}):failed to analyse configuration files. file={edns_conf_path}\n",
        f"[RESULT]:{mode}:{logtime_str}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00105, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:E00103, add_info:{edns_conf_path}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:設定ファイルJSON異常発生:\n",
        "パラメータ:\n",
        f" ファイルパス: {edns_conf_path}\n",
        f" Trace: JSONDecodeError filename: line 1 column 2 (char 1)\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.load = mocker.Mock(side_effect=[deepcopy(DICT_TOOL), deepcopy(DICT_SMFV), json.JSONDecodeError("filename", "test", 1)])
    mocker.patch("src.xcap_tool.json.load", test_mocker.load)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.load_config()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.load.called == True
    assert test_mocker.load.call_count == 3
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_load_config04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """load_config試験04 異常系試験 (必須キーなし)

    試験条件
    ・全設定ファイルを指定
    ・KeyError発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseであること
    ・json_check_and_loadが4回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down

    edns_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "edns-infos.json")

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({target.NF_NONE}):required json key not found. file={edns_conf_path}, key=edns_infos\n",
        f"[RESULT]:{mode}:{logtime_str}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00105, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:E00103, add_info:{edns_conf_path}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:設定ファイル必須キーなし発生:\n",
        "パラメータ:\n",
        f" ファイルパス: {edns_conf_path}\n",
        f" Trace: KeyError 'Key Error'\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.load = mocker.Mock(side_effect=[deepcopy(DICT_TOOL), deepcopy(DICT_SMFV), KeyError("Key Error")])
    mocker.patch("src.xcap_tool.json.load", test_mocker.load)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.load_config()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.load.called == True
    assert test_mocker.load.call_count == 3
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_load_config05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """load_config試験05 異常系試験 (想定外エラー)

    試験条件
    ・全設定ファイルを指定
    ・何らかのException発生

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がFalseであること
    ・json_check_and_loadが4回呼ばれること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down

    edns_conf_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("config", "edns-infos.json")

    expected_value = False
    tool_expected_value = "NG"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({target.NF_NONE}):unexpected error occurred. file={edns_conf_path}, key=edns_infos\n",
        f"[RESULT]:{mode}:{logtime_str}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00105, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:E00103, add_info:{edns_conf_path}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:想定外エラー発生:\n",
        "パラメータ:\n",
        f" ファイルパス: {edns_conf_path}\n",
        f" Trace: Exception Test Exception\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.load = mocker.Mock(side_effect=[deepcopy(DICT_TOOL), deepcopy(DICT_SMFV), Exception("Test Exception")])
    mocker.patch("src.xcap_tool.json.load", test_mocker.load)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.load_config()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert response_value == expected_value
    assert test_mocker.load.called == True
    assert test_mocker.load.call_count == 3
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_info01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """info試験01 正常試験 (OK)

    試験条件
    ・コマンド引数
        ・script_name = "xcap_tool.py"
        ・edns_name = "tys1tb1edns02"
        ・mode = Mode.down
        ・blocked_node = "a1-er-s01-amf-001,a2-er-s01-smfvo-001"
        ・batch = True
        ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・各コマンド引数が正常に取得できること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    script_name = "xcap_tool.py"
    edns_name = "tys1tb1edns02"
    mode = Mode.down
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    batch = True
    stub = False
    edns_ip_address = "2001:268:200d:1010::6"
    smfvoice_configs = {
        "a2-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        },
        "b1-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        }
    }

    expected_value = None

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        " eDNS Name: tys1tb1edns02\n",
        "   IP ADDR: 2001:268:200d:1010::6\n",
        "      MODE: DOWN\n",
        "   COMMENT: remove an xCAP ipaddr and add a reserved ipaddr\n",
        "BLOCKED NF: a1-er-s01-amf-001\n",
        "            a2-er-s01-smfvo-001\n",
        "     BATCH: True\n",
        "    TARGET: smfvo(roout) nf name    : [ipaddrs]\n",
        "            a2-er-s01-smfvoroout-001: ['2001:268:200d:1010::6', '2001:268:200d:5010::6', '2001:268:200d:500f::6']\n",
        "            b1-er-s01-smfvoroout-001: ['2001:268:200d:1010::6', '2001:268:200d:5010::6', '2001:268:200d:500f::6']\n",
        "\n",
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00107, add_info:{None}\n",
        *f"job_id:{JOB_ID}, message_id:I00108, add_info:{''.join(expected_sout[:-1])}\n".splitlines(True)
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.smfvoice_configs = smfvoice_configs
    tool.edns_ip_address = edns_ip_address
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.info()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_edns_ipaddr01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """get_edns_ipaddr試験01 正常系試験 (OK)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.down

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果が"2001:268:200d:1010::6"であること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS

    expected_value = "2001:268:200d:1010::6"

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00109, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00110, add_info:{expected_value}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.get_edns_ipaddr()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_edns_ipaddr02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """get_edns_ipaddr試験02 異常系試験 (NG, ValueError)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.down
    ・IP形式不備発生

    試験結果
    ・Exceptionが発生すること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down

    edns_ipaddr = "not ip format"
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = {
        "tys1tb1edns02": {
            "ipaddr": edns_ipaddr
        },
        "tys1tb2edns02": {
            "ipaddr": edns_ipaddr
        },
        "tys1tb3edns02": {
            "ipaddr": edns_ipaddr
        }
    }

    expected_value = None

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({target.NF_NONE}):eDNS configuration not found.\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00109, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:E00104, add_info:{edns_name}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:eDNS情報取得失敗:\n",
        "パラメータ:\n",
        f" eDNS: {edns_name}\n",
        f" INFO: {edns_ipaddr}\n",
        f" Trace: ValueError 'not ip format' does not appear to be an IPv4 or IPv6 address\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.ip_address = mocker.Mock(side_effect=[ValueError("%r does not appear to be an IPv4 or IPv6 address" % edns_ipaddr)])
    mocker.patch("ipaddress.ip_address", test_mocker.ip_address)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)

    with pytest.raises(Exception) as exc_info:
        response_value = tool.get_edns_ipaddr()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert isinstance(exc_info.value, ValueError)
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_get_edns_ipaddr03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """get_edns_ipaddr試験03 異常系試験 (NG, KeyError)

    試験条件
    ・edns_name = "tys1tb4edns02"
    ・mode = Mode.down
    ・対象eDNSなし

    試験結果
    ・Exceptionが発生すること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb4edns02"
    mode = Mode.down

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS

    edns_ipaddr = None

    expected_value = None

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({target.NF_NONE}):eDNS configuration not found.\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00109, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:E00104, add_info:{edns_name}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:eDNS情報取得失敗:\n",
        "パラメータ:\n",
        f" eDNS: {edns_name}\n",
        f" INFO: {edns_ipaddr}\n",
        f" Trace: KeyError 'tys1tb4edns02'\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)

    with pytest.raises(Exception) as exc_info:
        response_value = tool.get_edns_ipaddr()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert isinstance(exc_info.value, KeyError)
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_get_smfvoice_configs01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """get_smfvoice_configs試験01 正常系試験 (OK)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.down

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がSMFv情報の辞書であること
    ・標準出力がないこと
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down

    edns_ipaddr = "2001:268:200d:1010::6"
    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_infos"] = DICT_SMFV

    expected_value = DICT_SMFV

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = []

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00111, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00112, add_info:{expected_value}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.edns_ip_address = edns_ipaddr
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.get_smfvoice_configs()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_smfvoice_configs02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """test_get_smfvoice_configs02 get_smfvoice_configs試験02 異常系試験 (NG, ValueError)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.down
    ・対象SMFvなし

    試験結果
    ・Exceptionが発生すること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    edns_ipaddr = "2001:268:200d:1010::6"
    mode = Mode.down

    expected_value = None

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_infos"] = {
        "a2-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        },
        "b1-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        }
    }

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({target.NF_NONE}):smfvoice configuration not found.\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00111, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:E00105, add_info:{None}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:対向SMFv設定取得失敗:\n",
        "パラメータ:\n",
        f" eDNS: {edns_name}\n",
        f" 全SMFv: {tool_dict['nf_infos']}\n",
        f" Trace: ValueError filtered_list is empty.\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.edns_ip_address = edns_ipaddr
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)

    with pytest.raises(Exception) as exc_info:
        response_value = tool.get_smfvoice_configs()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert isinstance(exc_info.value, ValueError)
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_get_smfvoice_configs03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """get_smfvoice_configs試験03 異常系試験 (NG, KeyError)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.down
    ・xCAPキーなし

    試験結果
    ・Exceptionが発生すること
    ・関数結果がNoneであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力が想定しているlevel、add_infoであること
    """
    edns_name = "tys1tb1edns02"
    edns_ipaddr = "2001:268:200d:1010::6"
    mode = Mode.down

    expected_value = None

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["nf_infos"] = {
        "a2-er-s01-smfvoroout-001": {
        },
        "b1-er-s01-smfvoroout-001": {
        }
    }

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[ERROR]:{mode}:{logtime_str}:{edns_name}({target.NF_NONE}):smfvoice configuration not found.\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00111, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:E00105, add_info:{None}\n"
    ]

    expected_log_2nd = [
        f"job_id:{JOB_ID}, level:{Level.CRITICAL.name}, add_info:対向SMFv設定取得失敗:\n",
        "パラメータ:\n",
        f" eDNS: {edns_name}\n",
        f" 全SMFv: {tool_dict['nf_infos']}\n",
        f" Trace: KeyError 'xCAP'\n"
    ]

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.edns_ip_address = edns_ipaddr
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)

    with pytest.raises(Exception) as exc_info:
        response_value = tool.get_smfvoice_configs()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()
    with open(log_path_2nd, "r", encoding="utf-8") as f:
        response_value_log_2nd: List = f.readlines()

    assert isinstance(exc_info.value, KeyError)
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert log_path_2nd.exists()
    assert response_value_log_2nd == expected_log_2nd


def test_get_main01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験01 正常系試験 (LISTモード)

    試験条件
    ・edns_name = target.NF_NONE
    ・mode = Mode.list
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    ・batch = False
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = target.NF_NONE
    mode = Mode.list
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    batch = False
    stub = False

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS
    tool_dict["nf_infos"] = DICT_SMFV

    edns_name_list = [
        "tys1tb1edns02",
        "tys1tb2edns02",
        "tys1tb3edns02"
    ]

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "==eDNS LIST==\n",
        *[f" {x}\n" for x in edns_name_list]
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00115, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00116, add_info:{edns_name_list}\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_main02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験02 正常系試験 (INFOモード)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.info
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    ・batch = False
    ・stub = True

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.info
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    batch = False
    stub = True

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS
    tool_dict["nf_infos"] = DICT_SMFV

    edns_ipaddr = "2001:268:200d:1010::6"
    tool_expected_value = "OK"

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        "===== STUB MODE [ ON ] =====\n",
        f"[RESULT]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00122, add_info:{tool_expected_value}\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_edns_ipaddr = mocker.Mock(return_value=edns_ipaddr)
    test_mocker.get_smfvoice_configs = mocker.Mock(return_value=DICT_SMFV)
    test_mocker.info = mocker.Mock(return_value=None)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_edns_ipaddr", test_mocker.get_edns_ipaddr)
    mocker.patch.object(tool, "get_smfvoice_configs", test_mocker.get_smfvoice_configs)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_main03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験03 正常系試験 (SHOWモード, interactive: "n")

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.show
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    ・batch = False
    ・stub = False
    ・Y/N入力("n")

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.show
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    batch = False
    stub = False

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS
    tool_dict["nf_infos"] = DICT_SMFV

    edns_ipaddr = "2001:268:200d:1010::6"
    tool_expected_value = "OK"

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[INFO]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):script was aborted due to an interractive action.\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00123, add_info:n\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_edns_ipaddr = mocker.Mock(return_value=edns_ipaddr)
    test_mocker.get_smfvoice_configs = mocker.Mock(return_value=DICT_SMFV)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.interactive_check = mocker.Mock(return_value=(False, "n"))

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)
    mocker.patch("src.xcap_tool.interactive_check", test_mocker.interactive_check)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_edns_ipaddr", test_mocker.get_edns_ipaddr)
    mocker.patch.object(tool, "get_smfvoice_configs", test_mocker.get_smfvoice_configs)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_main04(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験04 正常系試験 (SHOWモード, エイリアス, interactive: "y")

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.show
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    ・batch = False
    ・stub = False
    ・Y/N入力("y")

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.show
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    batch = False
    stub = False

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS

    edns_ipaddr = "2001:268:200d:1010::6"
    smfvoice_configs = {
        "a2-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        },
        "b1-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        }
    }
    expected_success_list = ["a2-er-s01-smfvoroout-001", "b1-er-s01-smfvoroout-001"]
    expected_failed_list = []
    expected_blocked_list = []
    tool_expected_value = "OK"

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"Start Time: {logtime}\n",
        f"[RESULT]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):[ OK ]\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):"
        f"SUCCESS={len(expected_success_list)}, FAILED={len(expected_failed_list)}, BLOCKED={len(expected_blocked_list)}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):SUCCESSED NF {expected_success_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):FAILED NF {expected_failed_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):BLOCKED NF {expected_blocked_list}\n",
        f"End Time: {logtime}\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00117, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00118, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00119, add_info:{expected_success_list}\n",
        f"job_id:{JOB_ID}, message_id:I00120, add_info:{expected_failed_list}\n",
        f"job_id:{JOB_ID}, message_id:I00121, add_info:{expected_blocked_list}\n",
        f"job_id:{JOB_ID}, message_id:I00122, add_info:{tool_expected_value}\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_edns_ipaddr = mocker.Mock(return_value=edns_ipaddr)
    test_mocker.get_smfvoice_configs = mocker.Mock(return_value=smfvoice_configs)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.interactive_check = mocker.Mock(return_value=(True, "y"))
    test_mocker.Process = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.show_or_unknown)
    mocker.patch("src.xcap_tool.interactive_check", test_mocker.interactive_check)
    mocker.patch("src.xcap_tool.EriSmfvoXCAPProcess", test_mocker.Process)
    mocker.patch("tests.test_xcap_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_edns_ipaddr", test_mocker.get_edns_ipaddr)
    mocker.patch.object(tool, "get_smfvoice_configs", test_mocker.get_smfvoice_configs)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_main05(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験05 正常系試験 (downモード)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.down
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    ・batch = False
    ・stub = False

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    batch = True
    stub = False

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS

    edns_ipaddr = "2001:268:200d:1010::6"
    smfvoice_configs = {
        "a2-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        },
        "b1-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        }
    }
    expected_success_list = ["a2-er-s01-smfvoroout-001", "b1-er-s01-smfvoroout-001"]
    expected_failed_list = []
    expected_blocked_list = []
    tool_expected_value = "OK"

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"Start Time: {logtime}\n",
        f"[RESULT]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):"
        f"SUCCESS={len(expected_success_list)}, FAILED={len(expected_failed_list)}, BLOCKED={len(expected_blocked_list)}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):SUCCESSED NF {expected_success_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):FAILED NF {expected_failed_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):BLOCKED NF {expected_blocked_list}\n",
        f"End Time: {logtime}\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00117, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00118, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00119, add_info:{expected_success_list}\n",
        f"job_id:{JOB_ID}, message_id:I00120, add_info:{expected_failed_list}\n",
        f"job_id:{JOB_ID}, message_id:I00121, add_info:{expected_blocked_list}\n",
        f"job_id:{JOB_ID}, message_id:I00122, add_info:{tool_expected_value}\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_edns_ipaddr = mocker.Mock(return_value=edns_ipaddr)
    test_mocker.get_smfvoice_configs = mocker.Mock(return_value=smfvoice_configs)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.interactive_check = mocker.Mock(return_value=(True, "y"))
    test_mocker.Process = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.post_check_ok)
    mocker.patch("src.xcap_tool.interactive_check", test_mocker.interactive_check)
    mocker.patch("src.xcap_tool.EriSmfvoXCAPProcess", test_mocker.Process)
    mocker.patch("tests.test_xcap_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_edns_ipaddr", test_mocker.get_edns_ipaddr)
    mocker.patch.object(tool, "get_smfvoice_configs", test_mocker.get_smfvoice_configs)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_main06(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験06 準正常系試験 (DOWNモード, ProcessStatus.ssh_ng)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.down
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    ・batch = True
    ・stub = False
    ・EriSmfvoXCAPProcess.run=ProcessStatus.ssh_ng

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvoroout-001"]
    batch = True
    stub = False

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS
    tool_dict["nf_infos"] = DICT_SMFV

    edns_ipaddr = "2001:268:200d:1010::6"
    smfvoice_configs = {
        "a2-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        },
        "b1-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        }
    }
    expected_success_list = []
    expected_failed_list = ["b1-er-s01-smfvoroout-001"]
    expected_blocked_list = ["a2-er-s01-smfvoroout-001"]
    tool_expected_value = "NG"

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"Start Time: {logtime}\n",
        f"[RESULT]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):"
        f"SUCCESS={len(expected_success_list)}, FAILED={len(expected_failed_list)}, BLOCKED={len(expected_blocked_list)}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):SUCCESSED NF {expected_success_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):FAILED NF {expected_failed_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):BLOCKED NF {expected_blocked_list}\n",
        f"End Time: {logtime}\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00117, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00118, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00119, add_info:{expected_success_list}\n",
        f"job_id:{JOB_ID}, message_id:I00120, add_info:{expected_failed_list}\n",
        f"job_id:{JOB_ID}, message_id:I00121, add_info:{expected_blocked_list}\n",
        f"job_id:{JOB_ID}, message_id:I00122, add_info:{tool_expected_value}\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_edns_ipaddr = mocker.Mock(return_value=edns_ipaddr)
    test_mocker.get_smfvoice_configs = mocker.Mock(return_value=smfvoice_configs)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.Process = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.ssh_ng)
    mocker.patch("src.xcap_tool.EriSmfvoXCAPProcess", test_mocker.Process)
    mocker.patch("tests.test_xcap_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_edns_ipaddr", test_mocker.get_edns_ipaddr)
    mocker.patch.object(tool, "get_smfvoice_configs", test_mocker.get_smfvoice_configs)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_main07(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験07 準正常系試験 (DOWNモード, ProcessStatus.pre_check_ng)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.down
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    ・batch = True
    ・stub = False
    ・EriSmfvoXCAPProcess.run=ProcessStatus.pre_check_ng

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    batch = True
    stub = False

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS
    tool_dict["nf_infos"] = DICT_SMFV

    edns_ipaddr = "2001:268:200d:1010::6"
    smfvoice_configs = {
        "a2-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        },
        "b1-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        }
    }
    expected_success_list = []
    expected_failed_list = ["a2-er-s01-smfvoroout-001",  "b1-er-s01-smfvoroout-001"]
    expected_blocked_list = []
    tool_expected_value = "NG"

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"Start Time: {logtime}\n",
        f"[RESULT]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):"
        f"SUCCESS={len(expected_success_list)}, FAILED={len(expected_failed_list)}, BLOCKED={len(expected_blocked_list)}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):SUCCESSED NF {expected_success_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):FAILED NF {expected_failed_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):BLOCKED NF {expected_blocked_list}\n",
        f"End Time: {logtime}\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00117, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00118, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00119, add_info:{expected_success_list}\n",
        f"job_id:{JOB_ID}, message_id:I00120, add_info:{expected_failed_list}\n",
        f"job_id:{JOB_ID}, message_id:I00121, add_info:{expected_blocked_list}\n",
        f"job_id:{JOB_ID}, message_id:I00122, add_info:{tool_expected_value}\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_edns_ipaddr = mocker.Mock(return_value=edns_ipaddr)
    test_mocker.get_smfvoice_configs = mocker.Mock(return_value=smfvoice_configs)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.Process = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.pre_check_ng)
    mocker.patch("src.xcap_tool.EriSmfvoXCAPProcess", test_mocker.Process)
    mocker.patch("tests.test_xcap_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_edns_ipaddr", test_mocker.get_edns_ipaddr)
    mocker.patch.object(tool, "get_smfvoice_configs", test_mocker.get_smfvoice_configs)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_main08(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験08 準正常系試験 (DOWNモード, ProcessStatus.change_ng)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.down
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    ・batch = True
    ・stub = False
    ・EriSmfvoXCAPProcess.run=ProcessStatus.change_ng

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    batch = True
    stub = False

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS
    tool_dict["nf_infos"] = DICT_SMFV

    edns_ipaddr = "2001:268:200d:1010::6"
    smfvoice_configs = {
        "a2-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        },
        "b1-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        }
    }
    expected_success_list = []
    expected_failed_list = ["a2-er-s01-smfvoroout-001",  "b1-er-s01-smfvoroout-001"]
    expected_blocked_list = []
    tool_expected_value = "NG"

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"Start Time: {logtime}\n",
        f"[RESULT]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):"
        f"SUCCESS={len(expected_success_list)}, FAILED={len(expected_failed_list)}, BLOCKED={len(expected_blocked_list)}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):SUCCESSED NF {expected_success_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):FAILED NF {expected_failed_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):BLOCKED NF {expected_blocked_list}\n",
        f"End Time: {logtime}\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00117, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00118, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00119, add_info:{expected_success_list}\n",
        f"job_id:{JOB_ID}, message_id:I00120, add_info:{expected_failed_list}\n",
        f"job_id:{JOB_ID}, message_id:I00121, add_info:{expected_blocked_list}\n",
        f"job_id:{JOB_ID}, message_id:I00122, add_info:{tool_expected_value}\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_edns_ipaddr = mocker.Mock(return_value=edns_ipaddr)
    test_mocker.get_smfvoice_configs = mocker.Mock(return_value=smfvoice_configs)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.Process = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.change_ng)
    mocker.patch("src.xcap_tool.EriSmfvoXCAPProcess", test_mocker.Process)
    mocker.patch("tests.test_xcap_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_edns_ipaddr", test_mocker.get_edns_ipaddr)
    mocker.patch.object(tool, "get_smfvoice_configs", test_mocker.get_smfvoice_configs)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_main09(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験09 準正常系試験 (DOWNモード, ProcessStatus.post_check_ng)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.down
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    ・batch = True
    ・stub = False
    ・EriSmfvoXCAPProcess.run=ProcessStatus.post_check_ng

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    batch = True
    stub = False

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS
    tool_dict["nf_infos"] = DICT_SMFV

    edns_ipaddr = "2001:268:200d:1010::6"
    smfvoice_configs = {
        "a2-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        },
        "b1-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        }
    }
    expected_success_list = []
    expected_failed_list = ["a2-er-s01-smfvoroout-001",  "b1-er-s01-smfvoroout-001"]
    expected_blocked_list = []
    tool_expected_value = "NG"

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"Start Time: {logtime}\n",
        f"[RESULT]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):"
        f"SUCCESS={len(expected_success_list)}, FAILED={len(expected_failed_list)}, BLOCKED={len(expected_blocked_list)}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):SUCCESSED NF {expected_success_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):FAILED NF {expected_failed_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):BLOCKED NF {expected_blocked_list}\n",
        f"End Time: {logtime}\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00117, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00118, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00119, add_info:{expected_success_list}\n",
        f"job_id:{JOB_ID}, message_id:I00120, add_info:{expected_failed_list}\n",
        f"job_id:{JOB_ID}, message_id:I00121, add_info:{expected_blocked_list}\n",
        f"job_id:{JOB_ID}, message_id:I00122, add_info:{tool_expected_value}\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_edns_ipaddr = mocker.Mock(return_value=edns_ipaddr)
    test_mocker.get_smfvoice_configs = mocker.Mock(return_value=smfvoice_configs)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.Process = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.post_check_ng)
    mocker.patch("src.xcap_tool.EriSmfvoXCAPProcess", test_mocker.Process)
    mocker.patch("tests.test_xcap_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_edns_ipaddr", test_mocker.get_edns_ipaddr)
    mocker.patch.object(tool, "get_smfvoice_configs", test_mocker.get_smfvoice_configs)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_main10(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験10 準正常系試験 (DOWNモード, ProcessStatus.exception_ng)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.down
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    ・batch = True
    ・stub = False
    ・EriSmfvoXCAPProcess.run=ProcessStatus.exception_ng

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.down
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    batch = True
    stub = False

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS
    tool_dict["nf_infos"] = DICT_SMFV

    edns_ipaddr = "2001:268:200d:1010::6"
    smfvoice_configs = {
        "a2-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        },
        "b1-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        }
    }
    expected_success_list = []
    expected_failed_list = ["a2-er-s01-smfvoroout-001",  "b1-er-s01-smfvoroout-001"]
    expected_blocked_list = []
    tool_expected_value = "NG"

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"Start Time: {logtime}\n",
        f"[RESULT]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):"
        f"SUCCESS={len(expected_success_list)}, FAILED={len(expected_failed_list)}, BLOCKED={len(expected_blocked_list)}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):SUCCESSED NF {expected_success_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):FAILED NF {expected_failed_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):BLOCKED NF {expected_blocked_list}\n",
        f"End Time: {logtime}\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00117, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00118, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00119, add_info:{expected_success_list}\n",
        f"job_id:{JOB_ID}, message_id:I00120, add_info:{expected_failed_list}\n",
        f"job_id:{JOB_ID}, message_id:I00121, add_info:{expected_blocked_list}\n",
        f"job_id:{JOB_ID}, message_id:I00122, add_info:{tool_expected_value}\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_edns_ipaddr = mocker.Mock(return_value=edns_ipaddr)
    test_mocker.get_smfvoice_configs = mocker.Mock(return_value=smfvoice_configs)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.Process = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.exception_ng)
    mocker.patch("src.xcap_tool.EriSmfvoXCAPProcess", test_mocker.Process)
    mocker.patch("tests.test_xcap_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_edns_ipaddr", test_mocker.get_edns_ipaddr)
    mocker.patch.object(tool, "get_smfvoice_configs", test_mocker.get_smfvoice_configs)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_main11(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験11 異常系試験 (SHOWモード, eDNSアドレス取得失敗)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.show
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    ・batch = True
    ・stub = False
    ・対象eDNSアドレス取得失敗

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.show
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    batch = True
    stub = False

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS

    edns_ipaddr = "not ip format"
    smfvoice_configs = {
        "a2-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        },
        "b1-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        }
    }
    expected_success_list = []
    expected_failed_list = []
    expected_blocked_list = []
    tool_expected_value = "NG"

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[RESULT]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00122, add_info:{tool_expected_value}\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_edns_ipaddr = mocker.Mock(side_effect=ValueError("%r does not appear to be an IPv4 or IPv6 address" % edns_ipaddr))
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.exception_ng)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_edns_ipaddr", test_mocker.get_edns_ipaddr)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_main12(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験12 異常系試験 (SHOWモード, SMFv設定取得失敗)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.show
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    ・batch = True
    ・stub = False
    ・SMFv設定取得失敗

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.show
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001"]
    batch = True
    stub = False

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS

    edns_ipaddr = "2001:268:200d:1010::6"
    smfvoice_configs = {
        "a2-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        },
        "b1-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        }
    }
    expected_success_list = []
    expected_failed_list = []
    expected_blocked_list = []
    tool_expected_value = "NG"

    expected_value = False

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"[RESULT]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00122, add_info:{tool_expected_value}\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_edns_ipaddr = mocker.Mock(return_value=edns_ipaddr)
    test_mocker.get_smfvoice_configs = mocker.Mock(side_effect=ValueError("filtered_list is empty."))
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.exception_ng)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_edns_ipaddr", test_mocker.get_edns_ipaddr)
    mocker.patch.object(tool, "get_smfvoice_configs", test_mocker.get_smfvoice_configs)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_get_main13(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture):
    """main試験13 準正常系試験 (SHOWモード, 網閉塞中eDNSあり)

    試験条件
    ・edns_name = "tys1tb1edns02"
    ・mode = Mode.show
    ・blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001", "tys1tb3edns02"]
    ・batch = True
    ・stub = False
    ・網閉塞中eDNSあり

    試験結果
    ・Exceptionが発生しないこと
    ・関数結果がTrueであること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力が想定しているmsg_id、add_infoであること
    ・障害切り分けログ出力がないこと
    """
    edns_name = "tys1tb1edns02"
    mode = Mode.show
    blocked_nflist = ["a1-er-s01-amf-001", "a2-er-s01-smfvo-001", "tys1tb3edns02"]
    batch = True
    stub = False

    tool_dict = deepcopy(DICT_TOOL)
    tool_dict["edns_infos"] = DICT_EDNS

    edns_ipaddr = "2001:268:200d:1010::6"
    smfvoice_configs = {
        "a2-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6",
                "2001:268:200d:500f::6"
            ]
        },
        "b1-er-s01-smfvoroout-001": {
            "xCAP": [
                "2001:268:200d:1010::6",
                "2001:268:200d:5010::6"
            ]
        }
    }
    expected_success_list = ["a2-er-s01-smfvoroout-001", "b1-er-s01-smfvoroout-001"]
    expected_failed_list = []
    expected_blocked_list = []
    tool_expected_value = "OK"

    expected_value = True

    logtime = datetime(1994, 12, 3, 12, 34, 56)
    logtime_str = logtime.isoformat(sep=" ", timespec="seconds")

    expected_sout = [
        f"Start Time: {logtime}\n",
        f"[RESULT]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):[ {tool_expected_value} ]\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):"
        f"SUCCESS={len(expected_success_list)}, FAILED={len(expected_failed_list)}, BLOCKED={len(expected_blocked_list)}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):SUCCESSED NF {expected_success_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):FAILED NF {expected_failed_list}\n",
        f"[DETAIL]:{mode}:{logtime}:{edns_name}({target.NF_NONE}):BLOCKED NF {expected_blocked_list}\n",
        f"End Time: {logtime}\n"
    ]

    expected_log_1st = [
        f"job_id:{JOB_ID}, message_id:I00113, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00117, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00118, add_info:{None}\n",
        f"job_id:{JOB_ID}, message_id:I00119, add_info:{expected_success_list}\n",
        f"job_id:{JOB_ID}, message_id:I00120, add_info:{expected_failed_list}\n",
        f"job_id:{JOB_ID}, message_id:I00121, add_info:{expected_blocked_list}\n",
        f"job_id:{JOB_ID}, message_id:I00122, add_info:{tool_expected_value}\n",
        f"job_id:{JOB_ID}, message_id:I00114, add_info:{None}\n"
    ]

    expected_log_2nd = []

    logger = MockLog(JOB_ID, Level.INFO, log_dir=tmpdir)
    mocker.patch("src.xcap_tool.LOGGER", new=logger)

    test_mocker = mocker.MagicMock()
    test_mocker.edns_name = edns_name
    test_mocker.mode = mode
    test_mocker.blocked_nflist = blocked_nflist
    test_mocker.batch = batch
    test_mocker.stub = stub
    test_mocker.get_edns_ipaddr = mocker.Mock(return_value=edns_ipaddr)
    test_mocker.get_smfvoice_configs = mocker.Mock(return_value=smfvoice_configs)
    test_mocker.info = mocker.Mock(return_value=None)
    test_mocker.Process = mocker.Mock(return_value=MockProcess)
    test_mocker.run = mocker.Mock(return_value=ProcessStatus.show_or_unknown)
    mocker.patch("src.xcap_tool.EriSmfvoXCAPProcess", test_mocker.Process)
    mocker.patch("tests.test_xcap_tool.MockProcess.run", test_mocker.run)

    date_mock = mocker.MagicMock()
    date_mock.now = mocker.Mock(return_value=logtime)
    mocker.patch("src.abc_process.datetime", new=date_mock)

    tool = target.XcapTool()
    tool.args = None
    tool.tool_conf = tool_dict
    mocker.patch.object(tool, "args", test_mocker)
    mocker.patch.object(tool, "get_edns_ipaddr", test_mocker.get_edns_ipaddr)
    mocker.patch.object(tool, "get_smfvoice_configs", test_mocker.get_smfvoice_configs)
    mocker.patch.object(tool, "info", test_mocker.info)
    response_value = tool.main()

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)
    with open(log_path_1st, "r", encoding="utf-8") as f:
        response_value_log_1st: List = f.readlines()

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert log_path_1st.exists()
    assert response_value_log_1st == expected_log_1st
    assert not log_path_2nd.exists()


def test_interactive_check01(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch):
    """test_interactive_check01 interactive_check試験01 正常系試験 (interractive: "y")

    試験条件
    ・入力指示で「y」
    ・大文字小文字区別なし

    試験結果
    ・Exceptionが発生しないこと
    ・結果が(True, "y")となること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    message = "Please input [Y] for next action, or [N] for abort.: "
    continue_list = ["y", "ye", "yes"]
    abort_list = ["n", "no"]
    interact_input = "y"

    expected_value = (True, interact_input)

    expected_sout = [
        message
    ]

    expected_log_1st = []

    expected_log_2nd = []

    monkeypatch.setattr("sys.stdin", io.StringIO(interact_input + "\n"))
    response_value = target.interactive_check(message, continue_list, abort_list)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_interactive_check02(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch):
    """test_interactive_check02 interactive_check試験02 正常系試験 (interractive: "n")

    試験条件
    ・入力指示で「n」
    ・大文字小文字区別なし

    試験結果
    ・Exceptionが発生しないこと
    ・結果が(False, "n")となること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    message = "Please input [Y] for next action, or [N] for abort.: "
    continue_list = ["y", "ye", "yes"]
    abort_list = ["n", "no"]
    interact_input = "n"

    expected_value = (False, interact_input)

    expected_sout = [
        message
    ]

    expected_log_1st = []

    expected_log_2nd = []

    monkeypatch.setattr("sys.stdin", io.StringIO(interact_input + "\n"))
    response_value = target.interactive_check(message, continue_list, abort_list)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()


def test_interactive_check03(tmpdir, capsys: pytest.CaptureFixture, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch):
    """test_interactive_check03 interactive_check試験03 正常系試験 (interractive: "Y, y")

    試験条件
    ・入力指示で「Y」、「y」
    ・大文字小文字区別あり

    試験結果
    ・Exceptionが発生しないこと
    ・結果が(True, "y")となること
    ・標準出力が想定しているメッセージ内容であること
    ・一次ログ出力がないこと
    ・障害切り分けログ出力がないこと
    """
    message = "Please input [Y] for next action, or [N] for abort.: "
    continue_list = ["y", "ye", "yes"]
    abort_list = ["n", "no"]
    interact_input = ["Y", "y"]

    expected_value = (True, interact_input[1])

    expected_sout = [
        message + message
    ]

    expected_log_1st = []

    expected_log_2nd = []

    monkeypatch.setattr("sys.stdin", io.StringIO("\n".join(interact_input) + "\n"))
    response_value = target.interactive_check(message, continue_list, abort_list, True)

    # 結果確認
    (sout, serr) = capsys.readouterr()
    log_path_1st = get_1st_log_path(tmpdir)
    log_path_2nd = get_2nd_log_path(tmpdir)

    sout_desc: List = sout.splitlines(True)

    assert response_value == expected_value
    assert sout_desc == expected_sout
    assert not log_path_1st.exists()
    assert not log_path_2nd.exists()
