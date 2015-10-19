---
layout: post
title: "Dive into Linux Kernel IO Path"
tagline : "Dive into Linux Kernel IO Path"
description: "Dive into Linux Kernel IO Path"
category: "kernel"
tags: [kernel, linux, io]
---
{% include JB/setup %}

I want to understand the linux kernel IO path, by setup gdb debugging and step-by-step trace.

## Build Kernel

First I start up a centos 7 VM, which is my debug target, and built the kernel. To build custom centos 7 kernel, I followed the [official guide](https://wiki.centos.org/HowTos/Custom_Kernel). Remember to change kernel identifier in [step 4](https://wiki.centos.org/zh/HowTos/Custom_Kernel#head-adda851797ad4bf75277656ddf4cf28504a19967).

Kernel source will be at `~/rpmbuild/BUILD/kernel-*/linux-*/`. Kernel config is copied from existing OS `/boot/config-`uname -r`. Make sure below config options are enabled

  * The debug related options from [my blog](http://accelazh.github.io/kernel/Build-Linux-Kernel-and-Live-Debugging/)
  * KGDB related options from [ELinux KGDB](http://elinux.org/Kgdb)
  * Optionally Ftrace related options from [this blog](https://www.ibm.com/developerworks/community/blogs/58e72888-6340-46ac-b488-d31aa4058e9c/entry/exploring_the_linux_storage_path_tracing_block_i_o_kernel_events?lang=en)

It took me 3 hours to build kernel and 6GB disk space, put aside the time to install rpm. After it finishes, reboot, grub into the second `<your-kernel-identifier>.*.debug` kernel. It is the kernel you just built. If you want to debug kernel from boot, in grep press `e` and append kernel option `kgdbwait kgdboc=ttyS0,115200`. Then the kenrel will suspend before boot and wait for your gdb connection. Otherwise, the kernel boots normally. Then input below in shell to trigger a debug session. Note that I'm using serial port `ttyS0` to connect debug target and debug host.

```
echo ttyS0 > /sys/module/kgdboc/parameters/kgdboc
echo g > /proc/sysrq-trigger
```

The debug target should be suspended and wait for your gdb connection now. To connect, input below in your debug host VM. My debug host VM is a fedora VM with graphic desktop. The debug host VM should already have kernel source and `vmlinux` from where you built kernel. 

```
$ cd <kernel-source-dir>
$ cat gdbinit
set serial baud 115200
target remote /dev/ttyS0
$ gdb -x gdbinit vmlinux
```

The debug session should begin now. For complete guide, see [my blog](http://accelazh.github.io/kernel/Build-Linux-Kernel-and-Live-Debugging/) and find "Debug via Serial Port". I tried to setup Eclipse CDT + gdb remote debugging on my debug host VM. But it never worked. So I stick to gdb in shell commandline.

## A Program to Generate IO Writes

To generate IO writes, I wrote a program. There is only one C file which name is `loop_write.c`. It loops per several seconds to write something into a file, report its file descriptor `fd` and flushes. It flushes so that the writes would enter deeper block layer rather than stuck in kernel page cache. Below is my program

```
# my loop_write.c to generate writes periodically to fs
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

int main() {
    FILE* fp = NULL;
    int fd = 0;
    char templ[] = "Hello world I'm printing something here. Date = %u\n";
    unsigned int now = 0;
    int count = 0;

    fp = fopen("test.txt","at+");
    if (NULL == fp) {
        printf("Open file failed.\n");
        exit(1);
    }

    fd = fileno(fp);
    if (fd < 0) {
        printf("Cannot get fd.\n");
        exit(1);
    }
    printf("The file fd = %d\n", fd);
    printf("\n");
    fprintf(fp, "\nThe file fd = %d\n", fd);

    while (1) {
        now = (unsigned)time(NULL);
        fprintf(fp, templ, now);
        printf(templ, now);

        count++;
        fflush(fp);    // flush only the FILE* level
        printf("Flush the FILE* level.\n");
        if (count % 5 == 0) {   
            fsync(fd);    // tell OS to flush data to disk
            printf("Flush the OS level.\n");
        }
        printf("\n");
        sleep(5);
    }

    fclose(fp);
    return 0;
}
```

## Trace into the Rabbit Hole

Next I will start tracing into kernel IO path. My kernel version is `3.10.0-229.1.2.el7.centos.local_20151002.x86_64.debug`. The most helpful material is the linux kernel IO stack diagram from [Wikipedia](https://upload.wikimedia.org/wikipedia/commons/3/30/IO_stack_of_the_Linux_kernel.svg).

![Linux Kernel IO Stack](/images/linux-kernel-io-stack.svg "Linux Kernel IO Stack]")

Preparation steps

```
# on debug host VM, copy the kernel executable
$ cd <kenrel-souce-dir>
$ scp <debug-target>:~/rpmbuild/BUILD/kernel-3.10.0-229.1.2.el7/linux-3.10.0-229.1.2.el7.centos.local_20151007.x86_64/vmlinux

# on debug target VM, prepare the xfs module for gdb (since my loop_write.c writes to xfs)
$ lsmod | grep xfs    # you must make sure xfs module is loaded
xfs                   915019  2
libcrc32c              12644  1 xfs
$ ls /sys/module/xfs/    # to see runtime module files
$ cd /sys/module/xfs/sections/
$ cat .text .data .bss    # we will use the addresses later
0xffffffffa0144000
0xffffffffa0213000
0xffffffffa022b618
$ ls /lib/modules/3.10.0-229.1.2.el7.centos.local_20151002.x86_64.debug/kernel/fs/xfs/xfs.ko    # this is the xfs module executable (don't have debuginfo)

# on debug host VM, copy xfs.o
$ cd <kenrel-souce-dir>
$ scp <debug-target>:~/rpmbuild/BUILD/kernel-3.10.0-229.1.2.el7/linux-3.10.0-229.1.2.el7.centos.local_20151007.x86_64/fs/xfs/xfs.o ./fs/xfs/
$ #scp <debug-target>:/lib/modules/3.10.0-229.1.2.el7.centos.local_20151002.x86_64.debug/kernel/fs/xfs/xfs.ko ./fs/xfs/    # I once tried the .ko file, but it doesn't contain debuginfo

# on debug target VM, start my loop_write.c
cd ~/workspace/loop_write
gcc loop_write.c
nohup ./a.out 2>&1 1>a.out.log &
```

Dive into the FS layer. My fs under use is XFS.

```
# on debug target VM, start debugging (make sure you are at the local_20151002.*.debug kernel. and the debug host is using the correct version of kernel source)
$ echo ttyS0 > /sys/module/kgdboc/parameters/kgdboc
$ echo g > /proc/sysrq-trigger

# on debug host VM, start debug session
# tips: while debugging, avoid switching window to the debug target VM, otherwise gdb may be interrupted by received SYSTRAP signal (or other signals)
# tips: always delete unecessary breakpoints so that gdb will not catch irrelavent function calls
# tips: plug on the power for the laptop, otherwise I see my gdb session frequently interrupted by trap signals
# tips: if you recieve a SIGTRAP, 0x00000... in irq_stack_union () stuff, keep step `n`, it will get you back later

$ cd <kenrel-souce-dir>
$ gdb -x gdbinit vmlinux
# input 'break sys_write if (fd==3)', or input `break sys_write if (count==59)`, 59 is the loop_write.c message length
# input 'c', if you break on the right func call, the parameter `count` should be 59
fs\read_write.c::SYSCALL_DEFINE3(write, unsigned int, fd, const char __user *, buf, unsigned long, vlen)    # expand to sys_write(...). the n in SYSCALL_DEFINEn, should be argument count, I guess.
    ret = vfs_write(f.file, buf, count, &pos);
    # input `break vfs_write`
    # input `n`. gdb should be breaking at `vfs_write`
    # input `frame`, you should see `buf@entry` holds what loop_write.c prints to its file
         ret = file->f_op->write(file, buf, count, pos);
         # input 'delete breakpoint 1-2'    # to avoid catching irrelated func calls
         # input `break fs/read_write.c:466`    # just break on above line. if I don't do this, sometime gdb will go wrong
         # input 'c'
            fs/read_write.c::do_sync_write(..)
                # sync_write is actually implemented by aio_write
                ret = filp->f_op->aio_write(&kiocb, &iov, 1, kiocb.ki_pos);    # I'm using xfs. filp->f_op->aio_write == fs/xfs/xfs_file.c::xfs_file_operations.xfs_file_aio_write.
                
                # since xfs is a loadable module, rather than built into kernel, gdb cannot see or step into it on default. we need to load module symbols
                # to load module symbols, input `add-symbol-file ./fs/xfs/xfs.o 0xffffffffa0144000 -s .data 0xffffffffa0213000 -s .bss 0xffffffffa022b618`; input 'p xfs_file_aio_write' to verify
                # input 'break xfs_file_aio_write', then `s`. with the added module symols, I can not dive into xfs code
                
                    # when we have O_DIRECT, direct io will be launched
                    ret = xfs_file_dio_aio_write(iocb, iovp, nr_segs, pos, ocount);
                        ret = generic_file_direct_write(iocb, iovp, &nr_segs, pos, &iocb->ki_pos, count, ocount);
                            written = mapping->a_ops->direct_IO(WRITE, iocb, iov, pos, *nr_segs);    # points to fs/xfs/xfs_aops.c::xfs_vm_direct_IO
                                ret = __blockdev_direct_IO(rw, iocb, inode, bdev, iov, offset, nr_segs, xfs_get_blocks_direct, xfs_end_io_direct_write, NULL, 0);
                                    return do_blockdev_direct_IO(rw, iocb, inode, bdev, iov, offset, nr_segs, get_block, end_io, submit_io, flags);
                                        retval = do_direct_IO(dio, &sdio, &map_bh);
                                            ret = submit_page_section(dio, sdio, page, offset_in_page, this_chunk_bytes, sdio->next_block_for_io, map_bh);
                                                ret = dio_send_cur_page(dio, sdio, map_bh);
                                                    dio_bio_submit(dio, sdio);    # in fs/direct-io.c
                                                        submit_bio(dio->rw, bio);    # block/blk-core.c::submit_bio is the entrace from kernel FS layer to kernel block layer. I will trace that later.

                    # otherwise, buffered (buffered in kernel page cache) io will be launched
                    ret = xfs_file_buffered_aio_write(iocb, iovp, nr_segs, pos, ocount);
                        ret = generic_file_buffered_write(iocb, iovp, nr_segs, pos, &iocb->ki_pos, count, 0);
                            status = generic_perform_write(file, &i, pos);
                                struct address_space *mapping = file->f_mapping;    # `address_space` links current writing file to kernel page cache
                                const struct address_space_operations *a_ops = mapping->a_ops;    # where is the actual `address_space_operations` object assigned? it is defined at fs/xfs/xfs_aops.c::xfs_address_space_operations
                                
                                # a buffered write only needs to write data to kernel page cache
                                status = a_ops->write_begin(file, mapping, pos, bytes, flags, &page, &fsdata);    # points to fs/xfs/xfs_aops.c::xfs_address_space_operations.xfs_vm_write_begin
                                copied = iov_iter_copy_from_user_atomic(page, i, offset, bytes);
                                status = a_ops->write_end(file, mapping, pos, bytes, copied, page, fsdata);    # points to fs/xfs/xfs_aops.c::xfs_address_space_operations.xfs_vm_write_end
                                
                                # if there are too many dirty pages, flush to disk
                                balance_dirty_pages_ratelimited(mapping);    # defined at mm/page-writeback.c
                                    ...    # doing tests: do we really need to flush dirty pages?
                                    balance_dirty_pages(mapping, current->nr_dirtied);    # we are really going to flush dirty pages
                                        struct backing_dev_info *bdi = mapping->backing_dev_info;
                                        bdi_start_background_writeback(bdi);    # defined at fs/fs-writeback.c
                                            bdi_wakeup_thread(bdi);
                                                mod_delayed_work(bdi_wq, &bdi->wb.dwork, 0);    # push delayed_work `bdi->wb.dwork` to workqueue

    # so what is the `bdi->wb.dwork`?
    mm/backing-dev.c::bdi_wb_init(struct bdi_writeback *wb, struct backing_dev_info *bdi)
        INIT_DELAYED_WORK(&wb->dwork, bdi_writeback_workfn);   # so, `bdi->wb.dwork` is fs/fs-writeback.c::void bdi_writeback_workfn

                                                # continued from above
                                                mod_delayed_work(bdi_wq, &bdi->wb.dwork, 0);
                                                    
                                                    # async task executed by workqueue
                                                    fs/fs-writeback.c::bdi_writeback_workfn(struct work_struct *work)
                                                        pages_written = wb_do_writeback(wb);
                                                            wrote += wb_writeback(wb, work);
                                                                progress = writeback_sb_inodes(work->sb, wb, work);
                                                                    write_chunk = writeback_chunk_size(wb->bdi, work);
                                                                        ...    # just calc size, doesn't do actual io
                                                                    __writeback_single_inode(inode, &wbc);    # why the only lower level entrance I found is 'single' inode, no batch?
                                                                        ret = do_writepages(mapping, wbc);
                                                                            ret = mapping->a_ops->writepages(mapping, wbc);    # points to fs/xfs/xfs_aops.c::xfs_vm_writepages, defined at fs/xfs/xfs_aops.c::xfs_address_space_operations
                                                                                fs/xfs/xfs_aops.c::xfs_vm_writepages(struct address_space *mapping, struct writeback_control *wbc)
                                                                                    return generic_writepages(mapping, wbc);
                                                                                        ret = write_cache_pages(mapping, wbc, __writepage, mapping);
                                                                                            ret = (*writepage)(page, wbc, data);    # `writepage` points to mm/page-writeback.c::__writepage
                                                                                                int ret = mapping->a_ops->writepage(page, wbc);    # points to fs/xfs/xfs_aops.c::xfs_vm_writepage
                                                                                                    fs/xfs/xfs_aops.c::xfs_vm_writepage(struct page *page, struct writeback_control *wbc)
                                                                                                        bh = head = page_buffers(page);
                                                                                                        xfs_cluster_write(inode, page->index + 1, &imap, &ioend, wbc, end_index);    # looks like it doesn't actually do io
                                                                                                            done = xfs_convert_page(inode, pvec.pages[i], tindex++, imap, ioendp, wbc);    # allocate & map buffers
                                                                                                        xfs_submit_ioend(wbc, iohead, err);    # submit all of the bios
                                                                                                            bio = xfs_alloc_ioend_bio(bh);
                                                                                                            xfs_submit_ioend_bio(wbc, ioend, bio);
                                                                                                                submit_bio(wbc->sync_mode == WB_SYNC_ALL ? WRITE_SYNC : WRITE, bio);    # block/blk-core.c::submit_bio, the same end as the direct io path. here we eneters kernel block layer
```

Continuing from the above. Dive into the block layer.

```
# block/blk-core.c::submit_bio(..) is the entrace from kernel fs layer to kernel block layer.
# in the above section we traced kernel fs layer, the xfs filesystem (a kernel module). next we will trace into kernel block layer.

# let's start from block/blk-core.c::submit_bio (continuing from the fs layer gdb above)
block/blk-core.c::submit_bio(int rw, struct bio *bio)    # `struct bio` is defined at include/linux/blk_types.h and include/linux/bio.h.
    generic_make_request(bio);
        struct request_queue *q = bdev_get_queue(bio->bi_bdev);    # get our io queue of the current io device. `request_queue` is defined at blkdev.h
            return bdev->bd_disk->queue;    # `bdev_get_queue` is defined at include/linux/blkdev.h
        q->make_request_fn(q, bio);    # `make_request_fn` defined at blkdev.h
            block/blk-core.c::blk_queue_bio(struct request_queue *q, struct bio *bio)    # I digged out who is `make_request_fn` by gdb.

    # so which place assigned blk_queue_bio to q->make_request_fn?
    blk/blk-core.c::blk_init_queue(request_fn_proc *rfn, spinlock_t *lock)
        return blk_init_queue_node(rfn, lock, NUMA_NO_NODE);
            q = blk_init_allocated_queue(uninit_q, rfn, lock);
                blk_queue_make_request(q, blk_queue_bio);    # defined in block/blk-settings.c::blk_queue_make_request(struct request_queue *q, make_request_fn *mfn)
                    q->make_request_fn = mfn;

            # continued from above
            block/blk-core.c::blk_queue_bio(struct request_queue *q, struct bio *bio)  
                struct request *req;    # defined at include/linux/blkdev.h
                el_ret = elv_merge(q, &req, bio);    # `*req` is assigned. decide merge type (not actual merge), return ELEVATOR_NO_MERGE, ELEVATOR_BACK_MERGE or ELEVATOR_FRONT_MERGE (defined at include\linux\elevator.h).
                
                # if `el_ret` is ELEVATOR_BACK_MERGE or ELEVATOR_FRONT_MERGE
                bio_attempt_back_merge(q, req, bio)    # or bio_attempt_front_merge(q, req, bio). this one merges the `bio` rather than `req`
                    blk_account_io_start(req, false);
                elv_bio_merged(q, req, bio);
                    struct elevator_queue *e = q->elevator;    # `elevator_queue`, `elevator_ops` is defined at include/linux/elevator.h
                    e->type->ops.elevator_bio_merged_fn(q, rq, bio);    # these `q->elevator->type->op.*` are defined at block/*-iosched.c

    # what are those `q->elevator->type->op.*` functions? they are the linux io scheduler.
    # by `cat /sys/block/sda/queue/scheduler`, you can see (or change) your current kernel io scheduler, one from noop, anticipatory, deadline, or cfq.
    # take cfg as an example
    block/cfq-iosched.c::iosched_cfq = {
        .ops = {
            .elevator_merged_fn =       cfq_merged_request,
            .elevator_bio_merged_fn =   cfq_bio_merged,
            ...
        },
    }

                    # continued from above
                    e->type->ops.elevator_bio_merged_fn(q, rq, bio);    
                attempt_back_merge(q, req)    # or attempt_front_merge(q, req)
                    struct request *next = elv_latter_request(q, rq);
                    return attempt_merge(q, rq, next);    # this on merges `req` rather than `bio`
                        elv_merge_requests(q, req, next);
                        blk_account_io_merge(next);    # get statistics of the io merge
                            part = req->part;    # `part` is of type `hd_struct`, which is defined at include/linux/genhd.h
                elv_merged_request(q, req, el_ret);
                    struct elevator_queue *e = q->elevator;
                    e->type->ops.elevator_merged_fn(q, rq, type);    # see above

                # else if `el_ret` is ELEVATOR_NO_MERGE
                init_request_from_bio(req, bio);
                if (plug) {    # `struct blk_plug` is defined at include/linux/blkdev.h
                    list_add_tail(&req->queuelist, &plug->list);    # kernel plug feature to pool and batch io requests. here we just put new io request to plug list, instead of handling it immediately
                    blk_account_io_start(req, true);    # accounting io statistics
                } else {
                    add_acct_request(q, req, where);    # do accounting for this io request, and merge it to io queue
                        blk_account_io_start(rq, true);    # accounting io statistics
                        __elv_add_request(q, rq, where);    # add request to block io request queue. overall there are so many ways to elevator add an io request to our io queue
                            switch (where) {
                            case ELEVATOR_INSERT_REQUEUE, ELEVATOR_INSERT_FRONT:
                                list_add(&rq->queuelist, &q->queue_head);    # add `rq->queuelist` to `q->queue_head`
                            case ELEVATOR_INSERT_BACK:
                                list_add_tail(&rq->queuelist, &q->queue_head);
                                __blk_run_queue(q);    # we kick the queue here
                            case ELEVATOR_INSERT_SORT_MERGE:
                                elv_attempt_insert_merge(q, rq)
                            case ELEVATOR_INSERT_SORT:
                                q->elevator->type->ops.elevator_add_req_fn(q, rq);    # where and what is these elevator functions? see above iosched_cfq's
                            case ELEVATOR_INSERT_FLUSH:
                                blk_insert_flush(rq);
                            }
                    __blk_run_queue(q);
                        __blk_run_queue_uncond(q);
                            q->request_fn(q);    # handle the io requests in request queue `q` by each low level driver. this the gate from kernel block layer to kernel block driver layer
                                drivers/scsi/scsi_lib.c::scsi_request_fn(struct request_queue *q)    # how I digged out that 'scsi_request_fn' is the actual `request_fn`? since the exist of `plug`, I cannot directly step from `blk_queue_bio` to this line. so I break on `__blk_run_queue_uncond` and step into `q->request_fn(q)` to dig. By repeating many times I'm sure `scsi_request_fn` is it.
                            
    # so where is q->request_fn assigned? it is assigned in kernel block driver layer (the next lower layer under the block layer).
    # drivers under drivers/block/* (or some other places) invokes `blk_init_queue`. for example drivers/block/hd.c::hd_init.
    # different drivers assign different `request_fn`, i.e. it is driver specific
    # my debug target VM, which runs on virtualbox, uses `scsi_request_fn`. it is registed as following
    drivers/scsi/scsi_scan.c::scsi_alloc_sdev(struct scsi_target *starget, unsigned int lun, void *hostdata)
        sdev->request_queue = scsi_alloc_queue(sdev);
            q = __scsi_alloc_queue(sdev->host, scsi_request_fn);
                q = blk_init_queue(request_fn, NULL);
                    block/blk-core.c::blk_init_queue(request_fn_proc *rfn, spinlock_t *lock)
                        return blk_init_queue_node(rfn, lock, NUMA_NO_NODE);
                            q = blk_init_allocated_queue(uninit_q, rfn, lock);
                                q->request_fn       = rfn;

    # is there other places where `q->request_fn` is called? for example is there a async thread that keep handling requests in the io queue (I don't find answer)?
    # I searched the whole source directory, only `__blk_run_queue_uncond` calls to it.
    # digging the call hierarchy in reverse order ...
    q->request_fn(q);
        block/blk_core.c::__blk_run_queue_uncond(struct request_queue *q)
            block/blk_core.c::__blk_run_queue(struct request_queue *q)
                block/blk_core.c::__blk_drain_queue(struct request_queue *q, bool drain_all)    # looks like a invoke on `q->request_fn(q)` is enough to drain the complete queue
                ... # a lot of parent functions
            block/blk_exec.c::blk_execute_rq_nowait(struct request_queue *q, struct gendisk *bd_disk, struct request *rq, int at_head, rq_end_io_fn *done)
                blk_execute_rq(struct request_queue *q, struct gendisk *bd_disk, struct request *rq, int at_head)
                    block/scsi_ioctl.c::__blk_send_generic(struct request_queue *q, struct gendisk *bd_disk, int cmd, int data)
                        blk_send_start_stop(struct request_queue *q, struct gendisk *bd_disk, int data)
                            scsi_cmd_ioctl(struct request_queue *q, struct gendisk *bd_disk, fmode_t mode, unsigned int cmd, void __user *arg)    # scsi is much more complex than driver drivers/block/hd.c
                ... # a lot of parent functions
                                
                                drivers/scsi/scsi_lib.c::scsi_request_fn(struct request_queue *q)
```

Continuing from the above. Dive into the block driver layer. My block driver is SCSI.

```
# in the above section we traced the kernel block layer. next we will traced into kernel block driver layer. drivers/block/hd.c is a good example with only one file.
# but scsi is much more complex. my debug target VM uses scsi as the block driver. so I will dive into the scsi one. fisrt, I need to prepare kernel modules for gdb to see debuginfo

# on debug target VM prepare the scsi sd driver module for gdb
$ lsmod | grep sd
$ cd /sys/module/sd_mod/sections/
$ cat .text .data .bss
0xffffffffa0120000
0xffffffffa0129000
0xffffffffa0129998
$ ls /lib/modules/3.10.0-229.1.2.el7.centos.local_20151002.x86_64.debug/kernel/drivers/scsi/sd_mod.ko    # the sd module executable

# on debug target VM prepare the scsi mptspi driver module for gdb
$ lsmod | grep mptspi
$ cd /sys/module/mptspi/sections/
$ cat .text .data .bss
0xffffffffa00d3000
0xffffffffa00d7000
0xffffffffa00d7698
$ ls /lib/modules/3.10.0-229.1.2.el7.centos.local_20151002.x86_64.debug/kernel/drivers/message/fusion/mptspi.ko    # the mptspi driver is not under drivers/scsi/, weird

# on debug host VM, copy sd_mod.o and mptspi.o. if you don't have sd_mod.o, go to <debug-target>:<kernel-source-dir>, `make modules` to build
$ cd <kernel-source-dir>
$ scp <debug-target>:~/rpmbuild/BUILD/kernel-3.10.0-229.1.2.el7/linux-3.10.0-229.1.2.el7.centos.local_20151007.x86_64/drivers/scsi/sd_mod.o drivers/scsi/
$ scp <debug-target>:~/rpmbuild/BUILD/kernel-3.10.0-229.1.2.el7/linux-3.10.0-229.1.2.el7.centos.local_20151007.x86_64/drivers/message/fusion/mptspi.o drivers/message/fusion/

# my block driver layer uses scsi. but scsi it selves have drivers itselves again.
# scsi consists of high level drivers: sg, sr, sd, st. code at driver/scsi/* who defines a `struct scsi_driver` variable
# and low level drivers: there are a lot, e.g. fibre channel, SAS, iSCSI. code at drivers/scsi/* who defines a `struct scsi_host_template` variable. low level drivers are also called scsi host adapter drivers.

# I have to find which drivers I'm using. to find my disk major:minor numbers, `lsblk`.
# to find what high level scsi driver my disks are using
$ ll /sys/dev/block/*/device/driver
/sys/dev/block/8:0/device/driver -> ../../../../../../bus/scsi/drivers/sd
# in my case, my high level driver is the `sd` driver.
# when we `ls /dev/sd*`, the `sd` comes from here. in old times we have IDE drives which give /dev/hd*. but now we all use SCSI disks which give the /dev/sd*

# to find my low level scsi driver
$ udevadm info -a -n /dev/sda | grep -oP 'DRIVERS?=="\K[^"]+
sd
mptspi
# The second one, `mptspi` ,is my low level scsi driver.
# `lsscsi` is also a good tool
$ yum install -y lsscsi
$ lsscsi -Hlv    # to show scsi host info
$ lsscsi -t    # -t shows the transport I'm using - spi

# lets start from `scsi_request_fn` (continuing from fs layer and block layer gdb)
drivers/scsi/scsi_lib.c::scsi_request_fn(struct request_queue *q)
    for (;;) {
        req = blk_peek_request(q);
        cmd = req->special;
        rtn = scsi_dispatch_cmd(cmd);
            rtn = host->hostt->queuecommand(host, cmd);
            # we need to load kernel module symbols here
            # add-symbol-file ./drivers/scsi/sd_mod.o 0xffffffffa0120000 -s .data 0xffffffffa0129000 -s .bss 0xffffffffa0129998
            # add-symbol-file ./drivers/message/fusion/mptspi.o 0xffffffffa00d3000 -s .data 0xffffffffa00d7000 -s .bss 0xffffffffa00d7698
            # input `break mptspi_qcmd` to make it safer not to jump over
            # input `s`
                drivers/message/fusion/mptspi.c::mptspi_qcmd(struct Scsi_Host *shost, struct scsi_cmnd *SCpnt)    # my scsi low level driver here is mptspi
                    # input `delete break N` to delete prior break points to avoid unwanted catch
                    mptscsih_qcmd(SCpnt);
                        mpt_put_msg_frame(ioc->DoneCtx, ioc, mf);    # posts an MPT request frame to the request post FIFO of a specific MPT adapter
                            CHIPREG_WRITE32(&ioc->chip->RequestFifo, mf_dma_addr);    # there is a `#define CHIPREG_WRITE32(addr,val)   writel(val, addr)` and a `#include <asm/io.h>`
                                arch/x86/include/asm/io.h::writel(val, addr)    # links to include/asm-generic/io.h::'#define writel(b,addr) __raw_writel(__cpu_to_le32(b),addr)', I guess
                                    include/asm-generic/io.h::writel(b,addr)    # the '#define writel(b,addr) __raw_writel(__cpu_to_le32(b),addr)' links to below, I guess
                                        arch/x86/include/asm/io.h::__raw_writel(__cpu_to_le32(b),addr)    # there is a `#define __raw_writel __writel`
                                            arch/x86/include/asm/io.h::build_mmio_write(__writel, "l", unsigned int, "r", )    # the `build_mmio_write` macro defines `__writel`
                                                static inline void writel(unsigned val, volatile void __iomem *addr)     # note the `mf_dma_addr` above. so the assembles here are using DMA here.
                                                { asm volatile("mov" size " %0,%1": :"r" (val), \
                                                "m" (*(volatile unsigned int __force *)addr) ); }
    }
   
    # where does high level driver sc.d plays in? by searching `to_driver` in drivers/scsi I found below.
    # so I guess those high level drivers are high level, which interact with general scsi code, and low level drivers have no direct connection to them
    drivers\scsi\scsi.c::scsi_finish_command(struct scsi_cmnd *cmd)
        drv = scsi_cmd_to_driver(cmd);
    drivers\scsi\scsi_error.c::scsi_eh_action(struct scsi_cmnd *scmd, int rtn)
        struct scsi_driver *sdrv = scsi_cmd_to_driver(scmd);
    drivers\scsi\scsi_lib.c::scsi_prep_fn(struct request_queue *q, struct request *req)
        ret = scsi_cmd_to_driver(cmd)->init_command(cmd);
    drivers\scsi\scsi_lib.c::scsi_unprep_fn(struct request_queue *q, struct request *req)
        struct scsi_driver *drv = scsi_cmd_to_driver(cmd);


# since we write the scsi data by DMA, how do we handle the interrupt callback when it finishes? I found the irq handler mpt_interrupt(..)
# I'm not sure how mpt_interrupt(..) is registered as irq handler but the key entrace should be it
drivers/message/fusion/mptbase.c::mpt_interrupt(int irq, void *bus_id)
    mpt_reply(ioc, pa);
        freeme = MptCallbacks[cb_idx](ioc, mf, mr);    # invoke the IO callback
        # the io callback can be drivers/message/fusion/mptscsih.c::mptscsih_io_done(..), mptscsih_taskmgmt_complete(..), or mptscsih_scandv_complete(..). I will take :mptscsih_io_done as the example
            drivers/message/fusion/mptscsih.c::mptscsih_io_done(MPT_ADAPTER *ioc, MPT_FRAME_HDR *mf, MPT_FRAME_HDR *mr)
                switch(status) {
                case MPI_IOCSTATUS_SUCCESS:
                    sc->result = (DID_OK << 16) | scsi_status;
                }
                sc->scsi_done(sc);    # issue the command callback
                    drivers/scsi/scsi.c::scsi_done(struct scsi_cmnd *cmd)
                        blk_complete_request(cmd->request);
                            block/blk-softirq.c::blk_complete_request(struct request *req)
                                __blk_complete_request(struct request *req)
                                    list = this_cpu_ptr(&blk_cpu_done);    # the `static DEFINE_PER_CPU(struct list_head, blk_cpu_done);` defines `blk_cpu_done`
                                    list_add_tail(&req->ipi_list, list);    # the `req->ipi_list` is put into `blk_cpu_done` list

                                        # below is async invoked by BLOCK_SOFTIRQ. it is registered by `open_softirq(BLOCK_SOFTIRQ, blk_done_softirq);` at block/blk-softirq.c
                                        # I'm not sure how this BLOCK_SOFTIRQ is triggered or why we need a soft irq for block io completion. search "raise_softirq(BLOCK_SOFTIRQ" found nothing
                                        block/blk-softirq.c::blk_done_softirq(struct softirq_action *h)
                                            cpu_list = this_cpu_ptr(&blk_cpu_done);
                                            list_replace_init(cpu_list, &local_list);    # `local_list` now holds the local per cpu list `blk_cpu_done`
                                            while (!list_empty(&local_list)) {
                                                struct request *rq;
                                                rq = list_entry(local_list.next, struct request, ipi_list);
                                                list_del_init(&rq->ipi_list);
                                                rq->q->softirq_done_fn(rq);
                                                    drivers/scsi/scsi_lib.c::scsi_softirq_done(struct request *rq)    # I digged out who is the `softirq_done_fn` by gdb. it is assigned at drivers/scsi/scsi_lib.c::scsi_alloc_queue(struct scsi_device *sdev)
                                                        struct scsi_cmnd *cmd = rq->special;
                                                        scsi_finish_command(cmd);
                                                            scsi_io_completion(cmd, good_bytes);
                                                                blk_end_request_all(req, 0);
                                                                    pending = blk_end_bidi_request(rq, error, blk_rq_bytes(rq), bidi_bytes);
                                                                        blk_finish_request(rq, error);
                                                                            __blk_put_request(req->q, req);
                                                                                elv_completed_request(q, req);
                                                                                    freed_request(rl, flags);
                                                                                        __freed_request(rl, sync);
                                                                                            wake_up(&rl->wait[sync]);    # at block/blk-core.c::__freed_request(..)
                                            }

# remember the how fs/read_write.c::vfs_write(..) wait for aio to complete and wake up.
# I'm not sure how above `wake_up(&rl->wait[sync])` works to here the `atomic_read(&iocb->ki_users)`. but I guess that's it.
fs/read_write.c::vfs_write(struct file *file, const char __user *buf, size_t count, loff_t *pos)
    ret = do_sync_write(file, buf, count, pos);
        ret = filp->f_op->aio_write(&kiocb, &iov, 1, kiocb.ki_pos);
        ret = wait_on_sync_kiocb(&kiocb);    # here's how we wait for io to complete. defined at fs/aio.c
            while (atomic_read(&iocb->ki_users)) {
                set_current_state(TASK_UNINTERRUPTIBLE);
                if (!atomic_read(&iocb->ki_users))
                    break;
                io_schedule();
            }
            __set_current_state(TASK_RUNNING);
```

Come back to fs layer and study the kernel page cache

```
# next, let's go back to kernel fs later, and study the page cache `address_space` stuff
# remember that when we digging into `xfs_file_buffered_aio_write`, we step into this `generic_perform_write` function
mm/filemap.c::generic_perform_write(struct file *file, struct iov_iter *i, loff_t pos);
    # the `address_space` object is the bridge to kernel page cache.
    # inside the `address_space` defines a `struct radix_tree_root page_tree`
    # the kernel page cache is actually hold by the radix_tree.
    # radix tree is a space-optimized trie tree. for more see my references
    struct address_space *mapping = file->f_mapping;    # `address_space` is defined at include/linux/fs.h
    const struct address_space_operations *a_ops = mapping->a_ops;    # here the actual a_op is fs/xfs/xfs_aops.c::xfs_address_space_operations.
    
    # here is how we write user data to kernel page cache
    status = a_ops->write_begin(file, mapping, pos, bytes, flags, &page, &fsdata);    # step 1: use `address_space` to allocate / find proper pages on the kernel page cache, i.e. the `&page`. we will write the `&page`.
        fs/xfs/xfs_aops.c::xfs_vm_write_begin(struct file *file, struct address_space *mapping, loff_t pos, unsigned len, unsigned flags, struct page **pagep, void **fsdata)
            page = grab_cache_page_write_begin(mapping, index, flags);
                page = find_lock_page(mapping, index);
                    struct page *page = __find_lock_page(mapping, offset);
                        page = __find_get_page(mapping, offset);
                            pagep = radix_tree_lookup_slot(&mapping->page_tree, offset);     # now it is the radix tree stuff
                or page = __page_cache_alloc(gfp_mask & ~gfp_notmask);
            status = __block_write_begin(page, pos, len, xfs_get_blocks);    # some preparation work

    copied = iov_iter_copy_from_user_atomic(page, i, offset, bytes);    # step 2: copy user data the `page` which is actually backed by kernel page cache
        kaddr = kmap_atomic(page);
        left = __copy_from_user_inatomic(kaddr + offset, buf, bytes);
            arch/x86/include/asm/uaccess_64.h::__copy_from_user_inatomic(void *dst, const void __user *src, unsigned size)
                return copy_user_generic(dst, (__force const void *)src, size);
                    alternative_call_2(copy_user_generic_unrolled,    # call to low level asm code here
                            copy_user_generic_string,
                            X86_FEATURE_REP_GOOD,
                            copy_user_enhanced_fast_string,
                            X86_FEATURE_ERMS,
                            ASM_OUTPUT2("=a" (ret), "=D" (to), "=S" (from),
                                 "=d" (len)),
                            "1" (to), "2" (from), "3" (len)
                            : "memory", "rcx", "r8", "r9", "r10", "r11");
        kunmap_atomic(kaddr);
    
    status = a_ops->write_end(file, mapping, pos, bytes, copied, page, fsdata);    # step 3: end the writing and mark dirty
        fs/xfs/xfs_aops.c::xfs_vm_write_end(struct file *file, struct address_space *mapping, loff_t pos, unsigned len, unsigned copied, struct page *page, void *fsdata)
            ret = generic_write_end(file, mapping, pos, len, copied, page, fsdata);    # defined at fs/buffer.c
                copied = block_write_end(file, mapping, pos, len, copied, page, fsdata);
                    __block_commit_write(inode, page, start, start+copied);
                        set_buffer_uptodate(bh);
                        mark_buffer_dirty(bh);
                            __set_page_dirty(page, mapping, 0);    # defined at fs/buffer.c
                                radix_tree_tag_set(&mapping->page_tree, page_index(page), PAGECACHE_TAG_DIRTY);    # now it is the radix tree stuff
                                __mark_inode_dirty(mapping->host, I_DIRTY_PAGES);
    
    # next, if there are too many dirty pages, flush to disk
    balance_dirty_pages_ratelimited(mapping);    # defined at mm/page-writeback.c
        ...    # a greate bunch of function calls
            # the `writepages` here do actually write pages back to disk
            ret = mapping->a_ops->writepages(mapping, wbc);    # points to fs/xfs/xfs_aops.c::xfs_vm_writepages. 
                ...    # another greate bunch of function calls
                # the `writepage` here do actually write page back to disk
                int ret = mapping->a_ops->writepage(page, wbc);    # points to fs/xfs/xfs_aops.c::xfs_vm_writepage
                    ...    # yet another greate bunch of function calls
                        submit_bio(wbc->sync_mode == WB_SYNC_ALL ? WRITE_SYNC : WRITE, bio);    # block/blk-core.c::submit_bio, then entrace to kernel block layer
```

Things I'm still not clear about by now

```
1. in block driver layer, when writes finish and calls back, how BLOCK_SOFTIRQ is triggered and why we need it.
2. in block driver layer, when writes finish and calls back, in the end, how `wake_up(&rl->wait[sync])` works and how does fs/aio.c::wait_on_sync_kiocb(..) wake up on the right time
3. in block layer, is there an async thread keep processing block io requests in the request queue? I.e. an async thread keep calling block/blk_core.c::__blk_run_queue_uncond(..) { .. q->request_fn(q); ..}
```

Easy ways to piece together load module symbol commands for gdb

```
echo add-symbol-file ./fs/xfs/xfs.o $(cat /sys/module/xfs/sections/.text) -s .data $(cat /sys/module/xfs/sections/.data) -s .bss $(cat /sys/module/xfs/sections/.bss)
echo add-symbol-file ./drivers/scsi/sd_mod.o $(cat /sys/module/sd_mod/sections/.text) -s .data $(cat /sys/module/sd_mod/sections/.data) -s .bss $(cat /sys/module/sd_mod/sections/.bss)
echo add-symbol-file ./drivers/message/fusion/mptspi.o $(cat /sys/module/mptspi/sections/.text) -s .data $(cat /sys/module/mptspi/sections/.data) -s .bss $(cat /sys/module/mptspi/sections/.bss)
```

References

  * How to gdb into kernel module: [\[1\]](https://www.linux.com/learn/linux-training/33991-the-kernel-newbie-corner-kernel-and-module-debugging-with-gdb)[\[2\]](http://elinux.org/Debugging_The_Linux_Kernel_Using_Gdb#Debugging_a_kernel_module_.28.o_and_.ko_.29)
  * The Linux Storage Stack Diagram: [\[1\]](https://upload.wikimedia.org/wikipedia/commons/3/30/IO_stack_of_the_Linux_kernel.svg)
  * Dive into kernel filesystem IO path: [\[1\]](https://scaryreasoner.wordpress.com/2013/09/14/the-life-of-io-in-the-linux-kernel/)[\[2\]](http://blog.csdn.net/guogaofeng1219/article/details/5420468)[\[3\]](http://blog.csdn.net/guogaofeng1219/article/details/5411821)[\[4\]](http://blog.csdn.net/s1234567_89/article/details/7912979)[\[5\]](http://blog.csdn.net/s1234567_89/article/details/7915224)[\[6\]](http://alanwu.blog.51cto.com/3652632/1106506)
  * Kernel block level trace: [\[make_request_fn\]](https://www.win.tue.nl/~aeb/linux/vfs/trail-3.html)[\[request plug/unplug\]](http://blog.chinaunix.net/uid-14528823-id-4778396.html)
  * How to find which SCSI driver I'm using: [\[1\]](http://unix.stackexchange.com/questions/97676/how-to-find-the-driver-module-associated-with-a-device-on-linux)[\[2\]](http://stackoverflow.com/questions/17878843/determine-linux-driver-that-owns-a-disk)[\[3\]](http://sg.danny.cz/scsi/lsscsi.html)
  * IDE disk vs SCSI disk: [\[1\]](http://www.extremetech.com/computing/52680-top-tip-ide-or-scsi-which-is-better)
  * How SCSI IO subsystem works: [\[1\]](https://www.ibm.com/developerworks/cn/linux/l-cn-scsiio/)[\[2\]](http://www.ibm.com/developerworks/cn/linux/l-scsi-subsystem/)[\[3\]](http://www.uibk.ac.at/linuxdoc/LDP/HOWTO/html_single/SCSI-2.4-HOWTO/)[\[4\]](http://www.ibm.com/developerworks/library/l-scsi-api/)
  * SCSI high level driver vs low level driver: [[\[2\]](http://www.ibm.com/developerworks/cn/linux/l-scsi-subsystem/)[\[3\]](http://www.tldp.org/LDP/khg/HyperNews/get/devices/scsi.html)
  * Kernel Page Cache: [\[1\]](http://www.makelinux.net/books/lkd2/ch15lev1sec1)[\[2\]](http://www.ahlinux.com/start/kernel/6900.html)[\[3\]](http://www.makelinux.net/books/lkd2/ch15lev1sec2)[\[4\]](https://www.kernel.org/doc/Documentation/filesystems/vfs.txt)[\[5\]](http://blog.csdn.net/iter_zc/article/details/44195731)
  * Buffer Cache is Merged with Page Cache Now: [\[1\]](http://www.makelinux.net/books/lkd2/ch15lev1sec3)[\[2\]](https://www.quora.com/What-is-the-major-difference-between-the-buffer-cache-and-the-page-cache)
  * Page Cache Radix Tree: [\[1\]](http://blog.csdn.net/joker0910/article/details/8250085)[\[2\]](http://lwn.net/Articles/175432/)[\[3\]](http://www3.cs.stonybrook.edu/~porter/courses/cse506/f11/slides/page-cache-handout.pdf)[\[4\]](https://0xax.gitbooks.io/linux-insides/content/DataStructures/radix-tree.html)
