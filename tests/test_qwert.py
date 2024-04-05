#!/usr/bin/python

from pyln.testing.fixtures import *  # noqa: F403
from pyln.testing.utils import sync_blockheight
from util import get_plugin  # noqa: F401


def test_private_channel_receive(node_factory, bitcoind, get_plugin):  # noqa: F811
    l1, l2 = node_factory.get_nodes(
        2,
        opts={"plugin": get_plugin, "log-level": "io"},
    )
    l1.fundwallet(10_000_000)
    l2.fundwallet(10_000_000)
    l1.rpc.connect(l2.info["id"], "localhost", l2.port)
    l1.rpc.fundchannel(l2.info["id"], 1_000_000, mindepth=1)
    l2.rpc.fundchannel(l1.info["id"], 1_000_000, mindepth=1)

    bitcoind.generate_block(6)
    sync_blockheight(bitcoind, [l1, l2])

    result = l1.rpc.call("qwert")
    assert "version" in result
