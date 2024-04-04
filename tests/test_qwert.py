#!/usr/bin/python

from pyln.testing.fixtures import *  # noqa: F403
from pyln.testing.utils import only_one, sync_blockheight

def test_private_channel_receive(node_factory, bitcoind):  # noqa: F811
    l1, l2 = node_factory.get_nodes(
        2
    )
    l1.fundwallet(10_000_000)
    # setup 2 nodes with 1 private and 1 public channel
    l1.rpc.connect(l2.info["id"], "localhost", l2.port)
    scid_pub, _ = l1.fundchannel(l2, 1_000_000)
    bitcoind.generate_block(1)
    sync_blockheight(bitcoind, [l1, l2])
    scid_priv, _ = l1.fundchannel(
        l2, 1_000_000, announce_channel=False, push_msat=500_000_000
    )

    bitcoind.generate_block(6)
    sync_blockheight(bitcoind, [l1, l2])

    l1.wait_channel_active(scid_pub)
    l1.wait_local_channel_active(scid_priv)