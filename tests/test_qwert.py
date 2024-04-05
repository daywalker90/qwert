#!/usr/bin/python

import time

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


def test_pull_and_push(node_factory, bitcoind, get_plugin):  # noqa: F811
    l1, l2, l3 = node_factory.get_nodes(
        3, opts={"plugin": get_plugin, "log-level": "io"}
    )
    l1.fundwallet(10_000_000)
    l2.fundwallet(10_000_000)
    l3.fundwallet(10_000_000)
    l1.rpc.connect(l2.info["id"], "localhost", l2.port)
    l2.rpc.connect(l3.info["id"], "localhost", l3.port)
    l3.rpc.connect(l1.info["id"], "localhost", l1.port)
    l1.rpc.fundchannel(l2.info["id"], 1_000_000, mindepth=1, announce=True)
    l2.rpc.fundchannel(l3.info["id"], 1_000_000, mindepth=1, announce=True)
    l3.rpc.fundchannel(l1.info["id"], 1_000_000, mindepth=1, announce=True)

    bitcoind.generate_block(6)
    sync_blockheight(bitcoind, [l1, l2, l3])

    cl1 = l1.rpc.listpeerchannels(l2.info["id"])["channels"][0][
        "short_channel_id"
    ]
    cl2 = l2.rpc.listpeerchannels(l3.info["id"])["channels"][0][
        "short_channel_id"
    ]
    cl3 = l3.rpc.listpeerchannels(l1.info["id"])["channels"][0][
        "short_channel_id"
    ]

    for n in [l1, l2, l3]:
        for scid in [cl1, cl2, cl3]:
            n.wait_channel_active(scid)

    # wait for plugin gossip refresh
    time.sleep(2)


def test_stats(node_factory, bitcoind, get_plugin):  # noqa: F811
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

    chans = l2.rpc.listpeerchannels(l1.info["id"])["channels"]
    for chan in chans:
        if chan["opener"] == "local":
            cl2 = chan["short_channel_id"]
        else:
            cl1 = chan["short_channel_id"]
    l2.wait_channel_active(cl1)
    l2.wait_channel_active(cl2)


def test_pull_and_push2(node_factory, bitcoind, get_plugin):  # noqa: F811
    l1, l2, l3 = node_factory.get_nodes(
        3, opts={"plugin": get_plugin, "log-level": "io"}
    )
    l1.fundwallet(10_000_000)
    l2.fundwallet(10_000_000)
    l3.fundwallet(10_000_000)
    l1.rpc.connect(l2.info["id"], "localhost", l2.port)
    l2.rpc.connect(l3.info["id"], "localhost", l3.port)
    l3.rpc.connect(l1.info["id"], "localhost", l1.port)
    l1.rpc.fundchannel(l2.info["id"], 1_000_000, mindepth=1, announce=True)
    l2.rpc.fundchannel(l3.info["id"], 1_000_000, mindepth=1, announce=True)
    l3.rpc.fundchannel(l1.info["id"], 1_000_000, mindepth=1, announce=True)

    bitcoind.generate_block(6)
    sync_blockheight(bitcoind, [l1, l2, l3])

    cl1 = l1.rpc.listpeerchannels(l2.info["id"])["channels"][0][
        "short_channel_id"
    ]
    cl2 = l2.rpc.listpeerchannels(l3.info["id"])["channels"][0][
        "short_channel_id"
    ]
    cl3 = l3.rpc.listpeerchannels(l1.info["id"])["channels"][0][
        "short_channel_id"
    ]

    for n in [l1, l2, l3]:
        for scid in [cl1, cl2, cl3]:
            n.wait_channel_active(scid)

    # wait for plugin gossip refresh
    time.sleep(2)


def test_pull_and_push3(node_factory, bitcoind, get_plugin):  # noqa: F811
    l1, l2, l3 = node_factory.get_nodes(
        3, opts={"plugin": get_plugin, "log-level": "io"}
    )
    l1.fundwallet(10_000_000)
    l2.fundwallet(10_000_000)
    l3.fundwallet(10_000_000)
    l1.rpc.connect(l2.info["id"], "localhost", l2.port)
    l2.rpc.connect(l3.info["id"], "localhost", l3.port)
    l3.rpc.connect(l1.info["id"], "localhost", l1.port)
    l1.rpc.fundchannel(l2.info["id"], 1_000_000, mindepth=1, announce=True)
    l2.rpc.fundchannel(l3.info["id"], 1_000_000, mindepth=1, announce=True)
    l3.rpc.fundchannel(l1.info["id"], 1_000_000, mindepth=1, announce=True)

    bitcoind.generate_block(6)
    sync_blockheight(bitcoind, [l1, l2, l3])

    cl1 = l1.rpc.listpeerchannels(l2.info["id"])["channels"][0][
        "short_channel_id"
    ]
    cl2 = l2.rpc.listpeerchannels(l3.info["id"])["channels"][0][
        "short_channel_id"
    ]
    cl3 = l3.rpc.listpeerchannels(l1.info["id"])["channels"][0][
        "short_channel_id"
    ]

    for n in [l1, l2, l3]:
        for scid in [cl1, cl2, cl3]:
            n.wait_channel_active(scid)

    # wait for plugin gossip refresh
    time.sleep(2)


def test_pull_and_push4(node_factory, bitcoind, get_plugin):  # noqa: F811
    l1, l2, l3 = node_factory.get_nodes(
        3, opts={"plugin": get_plugin, "log-level": "io"}
    )
    l1.fundwallet(10_000_000)
    l2.fundwallet(10_000_000)
    l3.fundwallet(10_000_000)
    l1.rpc.connect(l2.info["id"], "localhost", l2.port)
    l2.rpc.connect(l3.info["id"], "localhost", l3.port)
    l3.rpc.connect(l1.info["id"], "localhost", l1.port)
    l1.rpc.fundchannel(l2.info["id"], 1_000_000, mindepth=1, announce=True)
    l2.rpc.fundchannel(l3.info["id"], 1_000_000, mindepth=1, announce=True)
    l3.rpc.fundchannel(l1.info["id"], 1_000_000, mindepth=1, announce=True)

    bitcoind.generate_block(6)
    sync_blockheight(bitcoind, [l1, l2, l3])

    cl1 = l1.rpc.listpeerchannels(l2.info["id"])["channels"][0][
        "short_channel_id"
    ]
    cl2 = l2.rpc.listpeerchannels(l3.info["id"])["channels"][0][
        "short_channel_id"
    ]
    cl3 = l3.rpc.listpeerchannels(l1.info["id"])["channels"][0][
        "short_channel_id"
    ]

    for n in [l1, l2, l3]:
        for scid in [cl1, cl2, cl3]:
            n.wait_channel_active(scid)

    # wait for plugin gossip refresh
    time.sleep(2)


def test_stats6(node_factory, bitcoind, get_plugin):  # noqa: F811
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

    chans = l2.rpc.listpeerchannels(l1.info["id"])["channels"]
    for chan in chans:
        if chan["opener"] == "local":
            cl2 = chan["short_channel_id"]
        else:
            cl1 = chan["short_channel_id"]
    l2.wait_channel_active(cl1)
    l2.wait_channel_active(cl2)
