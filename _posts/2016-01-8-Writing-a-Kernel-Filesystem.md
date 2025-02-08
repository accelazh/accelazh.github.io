---
layout: post
title: "Writing a Kernel Filesystem"
tagline : "Writing a Kernel Filesystem"
description: "Writing a Kernel Filesystem"
category: "Linux"
tags: [linux, kernel, filesystem]
---
{% include JB/setup %}

Linux filesystem works under the famous VFS model, and thus complies with POSIX. There are two ways to write a Linux filesystem

  * Fuse Filesystem
  * Kernel Filesystem

Fuse itself is a kernel filesystem. It forwards filesystem calls received from VFS to your custom program in userspace. The custom userspace program acts as the userspace filesystem for you to implement. See [wiki](https://en.wikipedia.org/wiki/Filesystem_in_Userspace).

![Fuse Structure](/images/fuse-structure.png "Fuse Structure")

To build a kernel filesystem, we implement a kernel module, which registers to VFS and implement its hooks. See [example](https://github.com/accelazh/hellofs/blob/dded64196c0959d1493bcace0d70365d70bf3e21/khellofs.c#L5-L32) below. VFS defines the common model of superblock, inode, dentry, file, and their operations. The hooks we registered define what an actual filesystem does.

```
struct file_system_type hellofs_fs_type = {
    .owner = THIS_MODULE,
    .name = "hellofs",
    .mount = hellofs_mount,
    .kill_sb = hellofs_kill_superblock,
    .fs_flags = FS_REQUIRES_DEV,
};

const struct super_operations hellofs_sb_ops = {
    .destroy_inode = hellofs_destroy_inode,
    .put_super = hellofs_put_super,
};

const struct inode_operations hellofs_inode_ops = {
    .create = hellofs_create,
    .mkdir = hellofs_mkdir,
    .lookup = hellofs_lookup,
};

const struct file_operations hellofs_dir_operations = {
    .owner = THIS_MODULE,
    .readdir = hellofs_readdir,
};

const struct file_operations hellofs_file_operations = {
    .read = hellofs_read,
    .write = hellofs_write,
};
```

My interesting findings are, 

  * Every text book tells linux filesystem uses inode, and inode saves data. What I find out is VFS concepts, such as superblock, inode, dentry, file, are only living in memory. You can actually design whatever you like on disk, with or without inode. The only thing you need is to make sure you construct VFS inode in memory and implement the hooks. The [struct inode](http://lxr.free-electrons.com/source/include/linux/fs.h?v=3.10#L521) even doesn't have a field to save data block.

  * The inode's direct and indirect data block structure, as [illustrated here](http://www.slideshare.net/tarnavski/how-inodes-work-presentation/9), are filesystem specific but now VFS specific. You can implement differet stuff as long as you can image.

The classic [Ext2 filesystem](http://lxr.free-electrons.com/source/fs/ext2/?v=3.10) is always used as an good example to learn how to write filesystem. The descendent Ext3, Ext4 basically follows the same style. Note that the above classic [direct/indirect data block structure](http://www.slideshare.net/tarnavski/how-inodes-work-presentation/9) also origins from Ext2. The disk layout of Ext2 is as follows

![Ext2 Layout](/images/ext2-layout.png "Ext2 Layout")

Ext2 uses bitmap to manage free and occupied inodes and data blocks. It uses an preallocated inode table to hold all the inodes allocated or to-be allocated. So one the filesystem is mkfs formatted, maximum inode count is fixed. You can at least tweak below parameters, according to how many files and how large files your filesystem is going to serve

  * Inode count: more inode count, more maximum file count, but less space available for data blocks. It is usefull if your filesystem is going to serve lots of small files.

  * Size of per inode: larger inode size means more direct data blocks. Althouth there are less space available for data blocks, but more file data can be put into direct blocks, and get accessed faster.

I found online resource about how to write a kernel filesystem are rare. Most of them are outdated (even still at 2.6). But the kernel is being rapidly developed (already 4.x). A working filesystem example is precious. Then I found [Simplefs](https://github.com/psankar/simplefs), which is awesome. However, my centos box doesn't have the jbd2 it required, and I don't quite agree with how Simplefs do inode and data block allocation.

So I rewrite based on Simplefs and build my [Hellofs](https://github.com/accelazh/hellofs). It should be a good example to get start with writting kernel filesystem. Welcome to take a look :-)