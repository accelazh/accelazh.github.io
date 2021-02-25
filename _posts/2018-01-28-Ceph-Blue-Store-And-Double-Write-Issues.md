---
layout: post
title: "Ceph BlueStore and Double Write Issues"
tagline : "Ceph BlueStore and Double Write Issues"
description: "Ceph BlueStore and Double Write Issues"
category: "ceph"
tags: [ceph, storage, bluestore]
---
{% include JB/setup %}

Summary of study, first published as a WeiChat article.

  * [Ceph BlueStore and Double Write Issues](https://mp.weixin.qq.com/s/dT4mr5iKnQi9-NEvGhI7Pg) [PDF](/images/ceph-bluestore-double-write-issue.pdf)

Besides, zhihu article [BlueStore源码分析之对象IO](https://zhuanlan.zhihu.com/p/92397191) by "鱼香肉丝没有鱼" has a nice chart of BlueStore IO path and code flow reading. Besides Ceph doc has a [BlueStore Small Write Strategies](https://github.com/ceph/ceph/blob/master/doc/dev/bluestore.rst).

![Ceph BlueStore Write IO Path](/images/ceph-bluestore-write-path-code-flow.jpg "Ceph BlueStore Write IO Path Code Flow")

In brief, Ceph BlueStore overcomes the double write issue by using append write rather than in-place write. In-place write, which destroys existing data, needs to be protected by transaction, thus need journaling/logging, i.e. a double write. Append write has no such needs. And further, metadata (keys) and data can be placed in separated places, where journaling/transaction only needs pointers to data.

There are a few BlueStore concepts to clear confusion

  * Small Write vs Big Write: A blob write is cut into two parts: 1) big part, i.e. multiple of min_alloc_size (HDD default 64K, SSD default 16K); 2) reminder part, less than min_alloc_size. Big part uses Big Write. Reminder part uses Small Write. Big Write is append-only, no double write. Small Write is more complex.

  * Overwrite vs Non-overwrite: Small Write next determines between the two 1) Writting to unused space - Non-overwrite; 2) Write overlaps with used space - Overwrite. For Non-overwrite, the write is in-place. There is no existing data to protect, so no double write needed.

  * Deferred Write: A Small Write that overwrites, can be merged in WAL to commit. Later, the Small Write in WAL is asynchronously moved to where it belongs in-place, i.e. deferred. Though overall double writes, in commit path there is one write. Batching small writes in journaling is a common technique.

Besides, a few common concepts

  * In-place write, Copy-on-Write, Delta append: Per writting a piece of new data, we have different strategies: 1) In-place overwrite the data; 2) Copy the original data, modify it with new data, and then append to a new place; 3) Only append data delta/diff to the new place

  * Read-modify-write, Read-modify-append: Per overwrite, when the modify size is smaller than the minimal block size, we need to read old block out, modify entire block with new data, and then write back. This is Read-modify-write.  Or instead of overwrite the modified data back, we can append it to a new place, i.e. Read-modify-append, which is same with Copy-on-Write.
