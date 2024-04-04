#!/usr/bin/python

from pyln.testing.fixtures import *  # noqa: F403
from pyln.testing.utils import only_one, sync_blockheight
from util import get_plugin  # noqa: F401

def test_private_channel_receive(node_factory, bitcoind, get_plugin):  # noqa: F811
    l1, l2 = node_factory.get_nodes(
        2, opts={"plugin": get_plugin}
    )
    l1.fundwallet(10_000_000)
    l1.rpc.connect(l2.info["id"], "localhost", l2.port)
    scid_pub, _ = l1.fundchannel(l2, 1_000_000)
    bitcoind.generate_block(1)
    sync_blockheight(bitcoind, [l1, l2])
    scid_pub2, _ = l1.fundchannel(l2, 1_000_000)

    bitcoind.generate_block(6)
    sync_blockheight(bitcoind, [l1, l2])

    l1.wait_channel_active(scid_pub)
    l1.wait_channel_active(scid_pub2)

    result = l1.rpc.call("qwert")
    assert("version" in result)