---
layout: post
title: "Ceph Code Deep Dive"
tagline : " Ceph Code Deep Dive"
description: "Ceph Code Deep Dive"
category: "Ceph"
tags: [ceph, storage, openstack]
---
{% include JB/setup %}

[Ceph](http://docs.ceph.com/docs/v0.78/architecture/) is great. It is a pure distributed storage system running on commodity hardware. The advantage compared to existing storage systems I summarized below are

  * Scale out with linear performance increase (theoretically) on large amount of nodes.
  * CRUSH map is highly customizable as related to object distribution and cluster layout.
  * The Monitor (internally uses Paxos) achieves cluster autonomous (auto recover of node fail, add/remove nodes, etc).
  * Converge filesystem storage, object storage and block/volume storage into one Ceph.
  * Ceph is high available, strong consistency, linear scalable, partition tolerant. Forget CAP.
  * The almost only one opensource, free, large-scale, stable, full-featured and easy-to-use distributed FS, object and block storage.
  * Highly (almost natively) integrated with Openstack (and Kubernetes, and other cloud platforms). Opensource community love ceph.
  * Ceph has good [papers](https://ceph.com/resources/publications/). Read that and you'll understand Ceph.

I will carry out a code deep dive into ceph next. The version is `firefly` V0.80 (I didn't remember the exact version but it should be OK).

## Ceph Monitor

Raw deep dive notes below. I will parse that into proper format and language when have time.

```
1. MonMap 结构很简单，就是
	epoch（整数）
	各个monitor的名字和ip地址

2. 可以研究的东西
	1. lockdep用来检测锁循环
	2. encode机制，有专门的文件encoding.h，用到了ceph::buffe::list

------------------------

1. KeyValueStore这一块
	LevelDBStore中，prefix其实是和key粘在了一起存进去了
	transaction其实是LevelDBStore的Batch操作
	compact指的是合并SSTable，就是LSM-Tree的标准操作
	Leveldb::DB的打开，在LevelDBStore::do_open()中
	MonitorDBStore底层用了LevelDBStore，其构造是文件路径path，在构造函数中传入。

1.1. Mon大量使用MonitorDBStore，即leveldb存储状态信息

2. Messenger这一块
	Dispatcher即指接收消息的人

3. Paxos
	Paxos.h定位是，paxos算法模型+消息发送，数据只是bytes
	PaxosService的定位是，有数据类型的paxos，并提供根据数据类型的一些方法，比如monmap
	尽管难懂，Paxos可以说是最extensively commented的代码了
	dispatch()函数往往是处理流程的核心吗？

   PaxosService->dispatch()->propose_pending()->encode_pending()

	PGMonitor的关键是pending_inc，从encode_pending()中寻找paxos要同步的数据
	OSDMonitor存有crushmap
		tick()中检查OSD状态，和do_propose

	What is MonSession?
	LogMonitor似乎比较简单，适合用来学习
	Tip: 可以通过跟踪state变量的变化，来学习Monitor.cc的代码
	PaxosService的一组类中，似乎不与messenger直接沟通。它们的dispatch()函数由Monitor.cc来调用的，在Monitor::dispatch()中。

4. Paxos规则
	ref: http://duanple.blog.163.com/blog/static/709717672011440267333/
	0. 角色和名词
		Proposer：意为提案者，它可以提出一个提案
		Proposal：提案，由Proposer提出。一个提案由一个编号及value形成的对组成，编号是为了防止混淆保证提案的可区分性，value即代表了提案本身的内容。
		
		Acceptor：是提案的受理者，有权决定是否它本身是否接受该提案
		Choose：提案被选定，在本文中当有半数以上Acceptor接受该提案时，就认为该提案被选定了，被选定的提案
		
		Learner：需要知道被选定的提案信息的那些人

	1. P1: 一个acceptor必须通过(accept)它收到的第一个提案。
	   P1a: 一个acceptor可以接受一个编号为n的提案，只要它还未响应任何编号大于n的prepare请求。

	2. P2: 如果具有value值v的提案被选定(chosen)了，那么所有比它编号更高的被选定的提案的value值也必须是v。
	   P2c: 对于任意的n和v，如果编号为n和value值为v的提案被提出，那么肯定存在一个由半数以上的acceptor组成的集合S，可以满足条件a)或者b)中的一个：
	   a)S中不存在任何的acceptor通过过编号小于n的提案。
	   b)v是S中所有acceptor通过的编号小于n的具有最大编号的提案的value值。
	   
	   P2c决定proposer如何产生proposal
	
	3. proposer如何产生proposal的算法：

		1. proposer选择一个新的提案编号n，然后向某个acceptors集合的成员发送请求，要求acceptor做出如下回应：
			(a).保证不再通过任何编号小于n的提案
			(b).当前它已经通过的编号小于n的最大编号的提案，如果存在的话

		2. 如果proposer收到了来自半数以上的acceptor的响应结果，那么它就可以产生编号为n，value值为v的提案，这里v是所有响应中编号最大的提案的value值，如果响应中不包含任何的提案那么这个值就可以由proposer任意选择。

		我们把这样的一个请求称为编号为n的prepare请求。

		Proposer通过向某个acceptors集合发送需要被通过的提案请求来产生一个提案(此时的acceptors集合不一定是响应prepare阶段请求的那个acceptors集合)。我们称此请求为accept请求。

	4. acceptor如何响应上述算法？

	   Acceptor可以忽略任何请求而不用担心破坏其算法的安全性。
	   Acceptor必须记住这些信息即使是在出错或者重启的情况下。
	   Proposer可以总是可以丢弃提案以及它所有的信息—只要它可以保证不会产生具有相同编号的提案即可。
	
	5.  将proposer和acceptor放在一块，我们可以得到算法的如下两阶段执行过程：

		Phase1.(a) proposer选择一个提案编号n，然后向acceptors的某个majority集合的成员发送编号为n的prepare请求。

		(b).如果一个acceptor收到一个编号为n的prepare请求，且n大于它已经响应的所有prepare请求的编号。那么它就会保证不会再通过(accept)任何编号小于n的提案，同时将它已经通过的最大编号的提案(如果存在的话)作为响应{!?此处隐含了一个结论，最大编号的提案肯定是小于n的}。

		Phase2.(a)如果proposer收到来自半数以上的acceptor对于它的prepare请求(编号为n)的响应，那么它就会发送一个针对编号为n，value值为v的提案的accept请求给acceptors，在这里v是收到的响应中编号最大的提案的值，如果响应中不包含提案，那么它就是任意值。

		(b).如果acceptor收到一个针对编号n的提案的accept请求，只要它还未对编号大于n的prepare请求作出响应，它就可以通过这个提案。	

	6. 很容易构造出一种情况，在该情况下，两个proposers持续地生成编号递增的一系列提案。
	   为了保证进度，必须选择一个特定的proposer来作为一个唯一的提案提出者。

	   如果系统中有足够的组件(proposer，acceptors及通信网络)工作良好，通过选择一个特定的proposer，活性就可以达到。著名的FLP结论指出，一个可靠的proposer选举算法要么利用随机性要么利用实时性来实现—比如使用超时机制。然而，无论选举是否成功，安全性都可以保证。{!即即使同时有2个或以上的proposers存在，算法仍然可以保证正确性}

	7. 不同的proposers会从不相交的编号集合中选择自己的编号，这样任何两个proposers就不会有相同编号的提案了。

	8. 关于leader election算法：http://csrd.aliapp.com/?p=162

-------------------------------------------------

1. monitor的paxos
	1. 所有的数据存在MonitorDBStore中，实际上是leveldb
	2. Paxos <- PaxosService <- MonmapService, OSDService ... <- Monitor

2. Monitor walkthrough
	[Mon0]
	init()
		bootstrap()
			state = STATE_PROBING
			send_message(new MMonProbe(OP_PROBE..)..)
	
	[Mon2]
	dispatch()
		handle_probe_probe()
			send_message(new MMonProbe(OP_REPLY..)..)
					

	[Mon0]
	dispatch()
		handle_proble_reply()
			if newer monmap
				use new monmap
				bootstrap()
			if ...
				bootstrap()
			if paxos->get_version() < m->paxos_first_version && m->paxos_first_version > 1 // my paxos verison is too low
				sync_start()
			if paxos->get_version() + g_conf->paxos_max_join_drift < m->paxos_last_version
				sync_start()
			if I'm part of cluster
				start_election()
			if outside_quorum.size() >= monmap->size() / 2 + 1
				start_election()
				
----------------------------------------------------------
	[election process] 编号小的mon胜利(entity_name_t._num,也是mon->rank)
		1. 每个Elector都向其它人发proposal，申请自己是leader
		2. 每个Elector收到proposal，leader_acked, m->get_source().num(), 自己mon->rank，谁小就defer到谁。
		   defer()会发送OP_ACK消息
		3. 收到ACK的Elector，会检查如果acked_me.size() == mon->monmap->size()，则victory()

	start_election()
		elector.call_election()
			 if (epoch % 2 == 0) 
			    bump_epoch(epoch+1)
			electing_me = true;
			broadcast to all
				send_message(new MMonElection(OP_PROPOSE, epoch, mon->monmap))

	Monitor.dispatch()
		case MSG_MON_ELECTION:
			elector.dispatch(m)
				if (peermap->epoch > mon->monmap->epoch)
					mon->monmap->decode(em->monmap_bl)
					mon->bootstrap()
				 switch (em->op)
					case MMonElection::OP_PROPOSE:
						handle_propose(em)
							if ignoring propose without required features
								nak_old_peer()
								return
							if (m->epoch > epoch)
								bump_epoch()
									mon->join_election()
							if (m->epoch < epoch) // got an "old" propose
								...
								return
							if (mon->rank < from) // i would win over them.
								...
							else 
								defer(from)
									send_message(new MMonElection(OP_ACK, epoch, mon->monmap), from)

	Elector.dispatch()
		case MMonElection::OP_ACK:
			handle_ack(em)
				if (m->epoch > epoch)
					bump_epoch(m->epoch);
    					start()
					return
				if (electing_me) // thanks
					 if (acked_me.size() == mon->monmap->size())
      						victory()
							change cmd set
							for each one
								send_message(new MMonElection(OP_VICTORY, epoch, mon->monmap), mon->monmap->get_inst(*p))
							mon->win_election()
								state = STATE_LEADER
								paxos->leader_init()
								monmon()->election_finished()
								
	Elector.dispatch()
		case MMonElection::OP_VICTORY:
			handle_victory()
				mon->lose_election()
				stash leader's commands


---------------------

1. Mon sync_start() 
/*同步的内容是paxos->get_version(), 整个

*/

[mon0]
sync_start()
	state = STATE_SYNCHRONIZING
	sync_provider = other
	send_message(new MMonSync(sync_full?OP_GET_COOKIE_FULL:OP_GET_COOKIE_RECENT), sync_provider)

[mon1]
dispatch()
	handle_sync_get_cookie()
		MMonSync *reply = new MMonSync(MMonSync::OP_COOKIE, sp.cookie);
  		reply->last_committed = sp.last_committed;
  		messenger->send_message(reply, m->get_connection());

[mon0]
dispatch()
	handle_sync()
		handle_sync_cookie()
			sync_cookie = m->cookie;
  			sync_start_version = m->last_committed;
  			MMonSync *r = new MMonSync(MMonSync::OP_GET_CHUNK, sync_cookie);
  			messenger->send_message(r, sync_provider);

[mon1]
dispatch()
	handle_sync()
		handle_sync_get_chunk()
			MMonSync *reply = new MMonSync(MMonSync::OP_CHUNK, sp.cookie);
			
			MonitorDBStore::Transaction tx;
			tx.put(paxos->get_name(), sp.last_committed, bl);
			sp.synchronizer->get_chunk_tx(tx, left);	// 拷贝整个MonitorDBStore
			::encode(tx, reply->chunk_bl);
			
			if no next chunk
				reply->op = MMonSync::OP_LAST_CHUNK;

			messenger->send_message(reply, m->get_connection());

[mon0]
dispatch()
	handle_sync()
		handle_sync_chunk()
			MonitorDBStore::Transaction tx;
			tx.append_from_encoded(m->chunk_bl);
			store->apply_transaction(tx);

			if OP_LAST_CHUNK
				sync_finish(m->last_committed);
					init_paxos();
					bootstrap();

---------------------------------------------------------

1. Paxos & PaxosService

	1. PaxosService::propose_pending()调用Paxos::propose_new_value()，称作commit。
	   MonmapService之类的都通过propose_ending()实现提交，不需要直接调用propose_new_value()。

	   propose_pending()中调用了encode_pendine()。
	   PaxosService::encode_pending()抽象函数，由子类覆盖。通过它能找到子类负责什么样的数据。

	2. Monitor::preinit()中，调用了
			paxos->init();
			for (int i = 0; i < PAXOS_NUM; ++i) {
				paxos_service[i]->init();
			}

  		Monitor::_reset中，调用了
  			paxos->restart();
  			for (vector<PaxosService*>::iterator p = paxos_service.begin(); p != paxos_service.end(); ++p)
    			(*p)->restart();

  		Monitor::win_election()中，调用了
  			paxos->leader_init()
  			monmon()->election_finished();
			for (vector<PaxosService*>::iterator p = paxos_service.begin(); p != paxos_service.end(); ++p) {
				if (*p != monmon())
					(*p)->election_finished();
			}

  		Monitor::lose_election()中，调用了
  			paxos->peon_init()
  			for (vector<PaxosService*>::iterator p = paxos_service.begin(); p != paxos_service.end(); ++p)
    			(*p)->election_finished();

1.5. Paxos leader collect
	leader_init()
		...
		collect(0);

	[mon0]
	collect(0)   //leader
		state = STATE_RECOVERING;
		
		// look for uncommitted value
  		if (get_store()->exists(get_name(), last_committed+1)) {
  			version_t v = get_store()->get(get_name(), "pending_v");
    		version_t pn = get_store()->get(get_name(), "pending_pn");
    		uncommitted_pn = pn;
    		uncommitted_v = last_committed+1;
    		get_store()->get(get_name(), last_committed+1, uncommitted_value);
    	}

    	// pick new pn
  		accepted_pn = get_new_proposal_number(MAX(accepted_pn, oldpn));

  		// send collect
  		for (set<int>::const_iterator p = mon->get_quorum().begin(); p != mon->get_quorum().end(); ++p) {
		    if (*p == mon->rank) continue;
		    
		    MMonPaxos *collect = new MMonPaxos(mon->get_epoch(), MMonPaxos::OP_COLLECT, ceph_clock_now(g_ceph_context));
		    collect->last_committed = last_committed;
		    collect->first_committed = first_committed;
		    collect->pn = accepted_pn;
		    mon->messenger->send_message(collect, mon->monmap->get_inst(*p));
		}

	[mon1]
	handle_collect()	//peon
		state = STATE_RECOVERING

		MMonPaxos *last = new MMonPaxos(mon->get_epoch(), MMonPaxos::OP_LAST, ceph_clock_now(g_ceph_context));
  		last->last_committed = last_committed;
  		last->first_committed = first_committed;

  		// can we accept this pn?
  		if (collect->pn > accepted_pn) {
  			accepted_pn = collect->pn;
  			MonitorDBStore::Transaction t;
  			t.put(get_name(), "accepted_pn", accepted_pn);
  		}

  		// share whatever committed values we have
  		if (collect->last_committed < last_committed)
    		share_state(last, collect->first_committed, collect->last_committed)	// 把我的过去多个commit放到了last中
    			for ( ; v <= last_committed; v++) {
					if (get_store()->exists(get_name(), v)) {
						get_store()->get(get_name(), v, m->values[v]);
					}
				}
    			m->last_committed = last_committed;

    	// do we have an accepted but uncommitted value?
  		//  (it'll be at last_committed+1)	
  		if (collect->last_committed <= last_committed && get_store()->exists(get_name(), last_committed+1)) {
  			get_store()->get(get_name(), last_committed+1, bl);
  			last->values[last_committed+1] = bl;
  			version_t v = get_store()->get(get_name(), "pending_v");
    		version_t pn = get_store()->get(get_name(), "pending_pn");
    		last->uncommitted_pn = pn;
  		}

  		// send reply
  		mon->messenger->send_message(last, collect->get_source_inst());

  	[mon0]
  	handle_last() 	// leader
  		// store any committed values if any are specified in the message
  		need_refresh = store_state(last);

  		// do they accept your pn?
  		if (last->pn > accepted_pn) {
  			// no, try again
  			collect(last->pn);
  		} else if (last->pn == accepted_pn) {
  			// yes, they do. great!
  			num_last++;

  			// did this person send back an accepted but uncommitted value?
  			if (last->uncommitted_pn) {
		    if (last->uncommitted_pn >= uncommitted_pn && last->last_committed >= last_committed && last->last_committed + 1 >= uncommitted_v) {
		    	// we learned an uncommitted value
				uncommitted_v = last->last_committed+1;
				uncommitted_pn = last->uncommitted_pn;
				uncommitted_value = last->values[uncommitted_v];
		      }
		    }

		    // is that everyone?
		    if (num_last == mon->get_quorum().size()) {
		    	// share committed values?
				for (map<int,version_t>::iterator p = peer_last_committed.begin(); p != peer_last_committed.end(); ++p) {
					if (p->second < last_committed) {
						// share committed values
					MMonPaxos *commit = new MMonPaxos(mon->get_epoch(), MMonPaxos::OP_COMMIT, ceph_clock_now(g_ceph_context));
					share_state(commit, peer_first_committed[p->first], p->second);
					mon->messenger->send_message(commit, mon->monmap->get_inst(p->first));
				}
		    }

		    // did we learn an old value?
      		if (uncommitted_v == last_committed+1 && uncommitted_value.length()) {
				state = STATE_UPDATING_PREVIOUS;
				begin(uncommitted_value);
			} else{
				finish_round();
					state = STATE_ACTIVE
			}

  		} else {
  			// this is an old message, discard
  		}

2. Paxos proposal
	PaxosService::dispatch(m)
		preprocess_query(PaxosServiceMessage* m)
		if (!mon->is_leader()) {
			mon->forward_request_leader(m);
			return true;
		}
		prepare_update(m)
		if (should_propose(delay)) {
      		if (delay == 0.0) {
				propose_pending();
      	}

    [mon0]
	PaxosService::propose_pending()
		Paxos::propose_new_value()
			queue_proposal(bl, onfinished);
			proposed_queued()
				C_Proposal *proposal = static_cast<C_Proposal*>(proposals.front());
				proposal->proposed = true;
				state = STATE_UPDATING;
				begin(proposal->bl);	//leader
					// accept it ourselves
  					accepted.clear();
  					accepted.insert(mon->rank);
  					new_value = v;

  					// store the proposed value in the store.
  					MonitorDBStore::Transaction t;
  					t.put(get_name(), last_committed+1, new_value);
  					t.put(get_name(), "pending_v", last_committed + 1);
  					t.put(get_name(), "pending_pn", accepted_pn);
  					get_store()->apply_transaction(t);

  					// ask others to accept it too!
					for (set<int>::const_iterator p = mon->get_quorum().begin(); p != mon->get_quorum().end(); ++p) {
						if (*p == mon->rank) continue;
						
						MMonPaxos *begin = new MMonPaxos(mon->get_epoch(), MMonPaxos::OP_BEGIN, ceph_clock_now(g_ceph_context));
						begin->values[last_committed+1] = new_value;
						begin->last_committed = last_committed;
						begin->pn = accepted_pn;
						
						mon->messenger->send_message(begin, mon->monmap->get_inst(*p));
					}

					// set timeout event
  					accept_timeout_event = new C_AcceptTimeout(this);
  					mon->timer.add_event_after(g_conf->mon_accept_timeout, accept_timeout_event); // 如果accept长时间未完成，则触发accept_timeout

	[mon1..n]
	handle_begin()	//peon
		if (begin->pn < accepted_pn) {return;}
		state = STATE_UPDATING;

		version_t v = last_committed+1;
		MonitorDBStore::Transaction t;
		t.put(get_name(), v, begin->values[v]);
		t.put(get_name(), "pending_v", v);
  		t.put(get_name(), "pending_pn", accepted_pn);
  		get_store()->apply_transaction(t);

  		MMonPaxos *accept = new MMonPaxos(mon->get_epoch(), MMonPaxos::OP_ACCEPT,
				    ceph_clock_now(g_ceph_context));
	  	accept->pn = accepted_pn;
	  	accept->last_committed = last_committed;
	  	mon->messenger->send_message(accept, begin->get_source_inst());


	[mon0]
	handle_accept()	//leader
		accepted.insert(from);
		// new majority?
		if (accepted.size() == (unsigned)mon->monmap->size()/2+1) {
			commit();
				MonitorDBStore::Transaction t;
				// commit locally
  				last_committed++;
  				last_commit_time = ceph_clock_now(g_ceph_context);
  				t.put(get_name(), "last_committed", last_committed);

  				for (set<int>::const_iterator p = mon->get_quorum().begin(); p != mon->get_quorum().end(); ++p) {
					if (*p == mon->rank) continue;

					MMonPaxos *commit = new MMonPaxos(mon->get_epoch(), MMonPaxos::OP_COMMIT, ceph_clock_now(g_ceph_context));
					commit->values[last_committed] = new_value;
					commit->pn = accepted_pn;
					commit->last_committed = last_committed;
					mon->messenger->send_message(commit, mon->monmap->get_inst(*p));
				}

			do_refresh()  // to notify PaxosService subclasses 
				...
			commit_proposal()
				C_Proposal *proposal = static_cast<C_Proposal*>(proposals.front());
				proposals.pop_front();
				proposal->complete(0);

		// done?
  		if (accepted == mon->get_quorum()) {
  			extend_lease();
  				lease_expire = ceph_clock_now(g_ceph_context);
  				lease_expire += g_conf->mon_lease;
  				acked_lease.clear();
  				acked_lease.insert(mon->rank);

				for (set<int>::const_iterator p = mon->get_quorum().begin(); p != mon->get_quorum().end(); ++p) {
					if (*p == mon->rank) continue;
					
					MMonPaxos *lease = new MMonPaxos(mon->get_epoch(), MMonPaxos::OP_LEASE, ceph_clock_now(g_ceph_context));
					lease->last_committed = last_committed;
					lease->lease_timestamp = lease_expire;
					lease->first_committed = first_committed;
					mon->messenger->send_message(lease, mon->monmap->get_inst(*p));
				}

  			finish_round();
  				state = STATE_ACTIVE;
  		}

  	[mon1..n]
  	handle_commit(MMonPaxos *commit)
  		store_state(commit)
  			start, end = ... // we want to write the range [last_committed, m->last_committed] only.
  			for (it = start; it != end; ++it) {
				t.put(get_name(), it->first, it->second);
				decode_append_transaction(t, it->second);
		    }
		    get_store()->apply_transaction(t);

  		do_refresh()

  	/*
  	I guess
  		last_committed表示paxos算法instance
  		version_t表示一个算法instance内，proposal的编号

  		如果accept长时间未完成，则触发accept_timeout
  		如果peon长时间为达成一致accept，那么extend_lease()就不会为它们执行，它们会发生lease_timeout

  		Monitor所用的paxos似乎是一种改进版的paxos。
  			首先保证有且仅有一个leader。
  			然后phase1只需要在leader初始时运行一次。
  			之后的propose只需要phase2。
  	*/

  	------------------ OP_LEASE process ----------------
  	[mon0]
  	extend_lease();	// extend lease of other mon

  	[mon1..n]
  	handle_lease()
  		lease_expire = lease->lease_timestamp;
  		state = STATE_ACTIVE;

		// ack
		MMonPaxos *ack = new MMonPaxos(mon->get_epoch(), MMonPaxos::OP_LEASE_ACK, ceph_clock_now(g_ceph_context));
		ack->last_committed = last_committed;
		ack->first_committed = first_committed;
		ack->lease_timestamp = ceph_clock_now(g_ceph_context);
		mon->messenger->send_message(ack, lease->get_source_inst());

		// (re)set timeout event.
  		reset_lease_timeout();

  	[mon0]
  	handle_lease_ack()
  		if (acked_lease == mon->get_quorum()) {
      		mon->timer.cancel_event(lease_ack_timeout_event);
      		lease_ack_timeout_event = 0;
      	}

    ---------------- OP_ACCEPT timeout ----------------

    void Paxos::accept_timeout()
		mon->bootstrap();

    -----------------How paxos value is read -----------------

    Paxos::handle_last() or handle_accept() or handle_commit() in the end
    	Paxos::do_refresh()
	    	mon->refresh_from_paxos(&need_bootstrap);
				for (int i = 0; i < PAXOS_NUM; ++i) {
					paxos_service[i]->refresh(need_bootstrap);
						// update cached versions
	  					cached_first_committed = mon->store->get(get_service_name(), first_committed_name);
	  					cached_last_committed = mon->store->get(get_service_name(), last_committed_name);

	  					update_from_paxos(need_bootstrap)			// implemented by subclasses, below use code of MonmapMonitor
	  						version_t version = get_last_committed();
	  						int ret = get_version(version, monmap_bl);	
	  						mon->monmap->decode(monmap_bl);
				}
				for (int i = 0; i < PAXOS_NUM; ++i) {
					paxos_service[i]->post_paxos_update()		// implemented by subclasses, below use code of MonmapMonitor
						// 什么都没写
				}


	/*
		假如不是MonmapMonitor的commit，MonmapMonitor也给refresh了怎么办？
			update_from_paxos()中get_version()对应的put_version()在encode_pending()中。
			get_version()并不是直接从paxos中拿，而是从get(get_service_name(), ver, bl)的get_service_name()中拿
	*/

	----------------- MonClient how to get ----------------

	MonClient::get_monmap()
		_sub_want("monmap", 0, 0);

		 while (want_monmap)
    		map_cond.Wait(monc_lock);

    [MonClient]
    MonClient::_reopen_session()
    	if (!sub_have.empty())
    		_renew_subs();
    			MMonSubscribe *m = new MMonSubscribe;
   				m->what = sub_have;
    			_send_mon_message(m);

    [Monitor]
    dispatch()
    	handle_subscribe()
    		for (map<string,ceph_mon_subscribe_item>::iterator p = m->what.begin(); p != m->what.end(); ++p){
    			session_map.add_update_sub(s, p->first, p->second.start, p->second.flags & CEPH_SUBSCRIBE_ONETIME, m->get_connection()->has_feature(CEPH_FEATURE_INCSUBOSDMAP));
    		}

    [OSDMonitor]
    OSDMonitor::update_from_paxos()
    	check_subs()
    		check_sub()
    			send_incremental(sub->next, sub->session->inst, sub->incremental_onetime);

    [MDSMonitor]
    同OSDMonitor

-------------------------

    [MonClient]
    MonClient::get_monmap_privately()
    	messenger->send_message(new MMonGetMap, cur_con)

    [Monitor]
    dispatch()
    	case CEPH_MSG_MON_GET_MAP:
      		handle_mon_get_map(static_cast<MMonGetMap*>(m));
      			send_latest_monmap(m->get_connection().get());
      				messenger->send_message(new MMonMap(bl), con);

    [MonClient]
    ms_dispatch()
    	case CEPH_MSG_MON_MAP:
    		handle_monmap(static_cast<MMonMap*>(m));
    			::decode(monmap, p);
    			map_cond.Signal();
```

The large state charts

![Ceph Monitor States](/images/ceph-monitor-states.png "Ceph Monitor States")

## Ceph OSD

Raw deep dive notes below. I will parse that into proper format and language when have time.

```
1. Context是回调函数
	C_Context这个类是把一组Context聚合成一个回调函数

2. coll_t实际上代表了一个目录，目录中是对象的集合
	ref: http://www.cnblogs.com/D-Tec/archive/2013/03/01/2939254.html

3. questions
	1. whay does sync do?
	2. why each store class implement themselves Transaction?
	3. what is omap?

4. MemStore
	1. queue_transaction()发起操作
	2. 操作由_do_transaction()完成
	3. MemStore中定义了自己的Collector类型和Object类型。数据结构是MemStore中存一个coll_t->Collection的map，Collection中存ghobject_t->Object的map。
	4. 父类ObjectStore中，只有coll_t，ghobject_t这样的东西，相当于id号，没有collection、object的实际数据结构，没有object_t出现。

5. ghobject_t
	1. 定义在hobject.h
	2. ghobject_t -> hobject_t -> object_t -> string name 可能就是一个文件路径

6. KeyValueStore
	Component: StripObjectMap -> GenericObjectMap->KeyValueDB
			   继承树：KeyValueDB
				    ->LevelDBStore
			   而MonitorDBStore内部使用了LevelDBStore
			   StripObjectMap中的KeyValueDB，是从构造函数中传入的
		
	在KeyValueStore中，StripObjectMap被称作backend
		GenericObjectMap似乎是围绕这header在搞
		header有parent属性
	
	throttle机制，KeyValueStore.cc line:1018，有借鉴意义
	
	queue_transactions()->op_queue_reserve_throttle()
	->queue_op()
	->op被放到OpSequencer中，->OpSequencer被OpWQ包一起来->OpWQ._enqueue()把OpSequence放入线程池ThreadPool
	->OpWQ._process()->KeyValueStore._do_op()->osr->peek_queue()取出op->_do_transactions(o->tls, o->op, &handle::TPHandle)
	->创建BufferTransaction->调用_do_transaction()，传入的是transaction而不是tls
	->终于能看见按op类型的switch case了

	->看一下_write()操作
	->BufferTransaction去lookup_cached_header->_generic_write()
	->file_to_extents()进行了strip分割
	-> ...

7. OSDMap中，包含了crush

8. questions
	1. how replication worked?
	2. how strong sync is achieved?
	3. snap shot how?
	4. osd gossip?
	5. osd auto recovery?
	6. what is the IO path?
	7. recovery and backfill process.
	8. snapshot process.
	9. what is OSD's superblock?
	10. what does OSDService do?
	11. what does PG's upgrade mean? seen in OSD::load_pgs()
	12. PG到底是怎么处理CephPeeringEvent的？
	13. OSD怎么做到增量写、thin provision的？
	14. split?
	15. what does pg's parent mean?
	16. what is the object's ondisk file/kv structure, including snap?
	    ref: https://ceph.com/docs/master/dev/osd_internals/snaps/
	17. what is object's generation

9. good points to learn
	1. how OSD/PG heartbeat is monitored
	2. how OSD health is monitored
	3. there are many checks and asserts embedded
	4. used a lot for waiting lists, such as OSD::waiting_for_osdmap, OSD::waiting_for_pg, OSD::pending_splits
	5. OSD::7531 -> op->mark_reached_pg(); 这追踪到TrackedOp::mark_event()。它最终写了一条日志，方便追踪op的轨迹。
	   我们可以借鉴它，不一定写日志，但追踪op的执行路径
	6. Messenger throttle机制
	   这是一个好的pattern。分布式存储系统中，如果recovery、scrubing、replication、rebalance等流量不加throttle，很可能significant performance regression
	7. reservation机制。
	   https://github.com/ceph/ceph/blob/master/doc/dev/osd_internals/backfill_reservation.rst
	   backfill reservation：如果所有的backfill同时发生，那么就会把目标机淹死。reservation使得同时进行的backfill数量得到限制。

10. 重复的pg
	1. 一个pg从属于一个pool
	2. 由pg_id、pg_t区分的一个pg，实际上是指有3份拷贝的一组pg
	   而3份拷贝中的每一份单独的pg，由spg_t类型表示

11. 可以研究的东西
	1. SafeTimer

12. material
	1. placement group states:
		http://ceph.com/docs/master/rados/operations/pg-states/

--------------------------------------------------------
[OSD Flow Tracing]

1. OSD msg dispatching

OSD::ms_dispatch()
	do_waiters()	// while !finished.empty(), do dispatch_op(next)
	_dispatch(m)
		// -- don't need lock --
		case CEPH_MSG_PING:
			break;
	
		// -- don't need OSDMap --
		case CEPH_MSG_OSD_MAP:
			handle_osd_map(static_cast<MOSDMap*>(m))
				to 2.1
		case CEPH_MSG_SHUTDOWN:
			shutdown();
		case MSG_PGSTATSACK:
			handle_pg_stats_ack(MPGStatsAck *ack)
				to 3.1
		case MSG_MON_COMMAND:
    		handle_command(static_cast<MMonCommand*>(m));
    			to 4
	  	case MSG_COMMAND:
    		handle_command(static_cast<MCommand*>(m));
    			to 4
    	case MSG_OSD_SCRUB:
			handle_scrub(static_cast<MOSDScrub*>(m));
			   	to 5.1
  		case MSG_OSD_REP_SCRUB:
    		handle_rep_scrub(static_cast<MOSDRepScrub*>(m));
    			to 5.4

		// -- need OSDMap --
		default:
			dispatch_op(op);

2. OSD OSDMap updating process

	2.1. when receive osd map message

		handle_osd_map(static_cast<MOSDMap*>(m))
			if (first > osdmap->get_epoch() + 1)	// missing some epoch of OSDMap
				osdmap_subscribe(..)				

			// store new maps: queue for disk and put in the osdmap cache
			for (epoch_t e = start; e <= last; e++)
				t.write(coll_t::META_COLL, fulloid, 0, bl.length(), bl);

			// update superblock
			superblock.oldest_map = first;
			superblock.newest_map = last;

			// advance through the new maps
			for (epoch_t cur = start; cur <= superblock.newest_map; cur++)
				// start blacklisting messages sent to peers that go down.
			service.pre_publish_map(newmap);

			// kill connections to newly down osds
			...

			osdmap = newmap;

			advance_map(t, fin);	// since crushmap is different now, I need update my pg
				ceph::unordered_map<spg_t, create_pg_info>::iterator n = creating_pgs.begin();
				while (n != creating_pgs.end())
					// am i still primary?
					if (primary != whoami)
						creating_pgs.erase(p);

				// scan for waiting_for_pg
				map<spg_t, list<OpRequestRef> >::iterator p = waiting_for_pg.begin();
					while (p != waiting_for_pg.end())
						int role = osdmap->calc_pg_role(whoami, acting, nrep);		// my osd rank in the pg's acting osds
						...

			// the only place to change state = ACTIVE
			if (is_booting())
				state = ACTIVE

			// check am I in osdmap? 
			if state == ACTIVE
				if (!osdmap->exists(whoami))
					do_shutdown = true
				else if (!osdmap->is_up(whoami) || addr wrong) 		// if something wrong
					... stop, or start_waiting_for_healthy()

			// superblock and commit
			write_superblock(t);
			store->queue_transaction(0, _t, new C_OnMapApply(&service, _t, pinned_maps, osdmap->get_epoch()), 0, fin);
			service.publish_superblock(superblock);

			// yay!
			consume_map();
				// scan pg's, to count num_pg_primary, num_pg_replica, num_pg_stray, and find which pg need to be removed
				for (ceph::unordered_map<spg_t,PG*>::iterator it = pg_map.begin(); it != pg_map.end()
					...
				// remove pg
				for (..)
					_remove_pg(&**i);
				// scan pg's
				for (ceph::unordered_map<spg_t,PG*>::iterator it = pg_map.begin(); it != pg_map.end()
					pg->queue_null(osdmap->get_epoch(), osdmap->get_epoch());


			if (!is_active()) {
				peering_wq.drain();
			} else {
				activate_map();
					wake_all_pg_waiters();
					// norecover?
					...
					service.activate_map();
			}

			// end
			if (m->newest_map && m->newest_map > last) {
				osdmap_subscribe(osdmap->get_epoch()+1, true);
			} else if (is_booting()) {
				start_boot();  // retry
			} else if (do_restart)
				start_boot();

			if (do_shutdown)
				shutdown();

	2.2. where osdmap is sent out 

		handle_replica_op() or handle_op()
			_share_map_incoming(..)
				send_incremental_map(epoch, con)

		handle_osd_ping() or do_notifies() or do_queries() or do_infos() or handle_pg_query()
			_share_map_outgoing(..)
				send_incremental_map(pe, con)				
	
3. send pg status to mon, and receive pg status ack on osd

	3.1. when MSG_PGSTATSACK comes

		handle_pg_stats_ack(MPGStatsAck *ack)
				if (!require_mon_peer(ack))
					return;		// the other end of msg must be mon
				xlist<PG*>::iterator p = pg_stat_queue.begin();
  				while (!p.end())
  					pg->stat_queue_item.remove_myself();

  	3.2. where MSG_PGSTATSACK sends out

  		in OSD.cc
  		flush_pg_stats() or do_mon_report() or ms_handle_connect()
  		send_pg_stats(..)
  			MPGStats *m = new MPGStats(monc->get_fsid(), osdmap->get_epoch(), had_for);
  			xlist<PG*>::iterator p = pg_stat_queue.begin();
  			while (!p.end())
  				if (pg->pg_stats_publish_valid)
  					m->pg_stat[pg->info.pgid.pgid] = pg->pg_stats_publish;

  			monc->send_mon_message(m);

  		in PGMonitor.cc
  		prepare_update(PaxosServiceMessage *m)
  			case MSG_PGSTATS:
  				return prepare_pg_stats((MPGStats*)m);
  					MPGStatsAck *ack = new MPGStatsAck;
  					...
  					mon->send_reply(stats, ack);

  			case MSG_MON_COMMAND:
  				...

4. handle command 

	handle_command(static_cast<MMonCommand*>(m)) or handle_command(static_cast<MCommand*>(m));
		command_wq.queue(c);

	OSD::CommandWQ
		void _process(Command *c)
			osd->do_command(c->con.get(), c->tid, c->cmd, c->indata);
				... 	// handle cli commands
				MCommandReply *reply = new MCommandReply(r, rs);
				client_messenger->send_message(reply, con);

5.  scrubbing process

	5.1. handle MSG_OSD_SCRUB
		handle_scrub(MOSDScrub *m)
			if (!require_mon_peer(m))		// must be sent from mon
	    		return;
	    	
	    	if (m->scrub_pgs.empty())
	    		for (ceph::unordered_map<spg_t, PG*>::iterator p = pg_map.begin(); p != pg_map.end(); ++p)
	    			if (pg->is_primary())
	    				pg->unreg_next_scrub();
	    				pg->scrubber.must_scrub = true;
	    				pg->reg_next_scrub();
	    					osd->reg_last_pg_scrub(info.pgid, scrubber.scrub_reg_stamp);
	    						last_scrub_pg.insert(pair<utime_t,spg_t>(t, pgid));
	    	else
	    		for (vector<pg_t>::iterator p = m->scrub_pgs.begin(); p != m->scrub_pgs.end(); ++p)
	    			if (osdmap->get_primary_shard(*p, &pcand) && pg_map.count(pcand)
	    				PG *pg = pg_map[pcand];			// to get primary pg
	    			if (pg->is_primary())
	    				pg->unreg_next_scrub();
	    				pg->scrubber.must_scrub = true;
	    				pg->reg_next_scrub();

	5.2. when will last_scrub_pg be cancelled

		OSD::handle_scrub(MOSDScrub *m) or ReplicatedPG::on_shutdown()
			PG::unreg_next_scrub()
				osd->unreg_last_pg_scrub(info.pgid, scrubber.scrub_reg_stamp);		// OSDService::unreg_last_pg_scrub(spg_t pgid, utime_t t)
					last_scrub_pg.erase(it);

	5.3. when will scrubbing happen

		OSD::sched_scrub()
			pg->sched_scrub()
				queue_scrub();
					state_set(PG_STATE_SCRUBBING);
					osd->queue_for_scrub(this);
						scrub_wq.queue(pg);

		OSD::ScrubWQ
			void _process(..)
				pg->scrub(handle);
					if (!is_primary() || !is_active() || !is_clean() || !is_scrubbing()) {
					    state_clear(PG_STATE_SCRUBBING);
					    state_clear(PG_STATE_REPAIR);
					    state_clear(PG_STATE_DEEP_SCRUB);
					    publish_stats_to_osd();
					    return;
					}

					// when we're starting a scrub, we need to determine which type of scrub to do
					if (!scrubber.active)
						scrubber.is_chunky = true;
						if (!con->has_feature(CEPH_FEATURE_CHUNKY_SCRUB))
							scrubber.is_chunky = false;

					// do scrubbing
					if (scrubber.is_chunky) {
						chunky_scrub(handle);
					} else {
						classic_scrub(handle);
					}

		/*
			the next scrubbing process is handled by PG::Scrubber
			the process is a bit complex
		*/

	5.4. handle MSG_OSD_REP_SCRUB
		handle_rep_scrub(static_cast<MOSDRepScrub*>(m))		//rep means replica
		 	rep_scrub_wq.queue(m);

		 OSD::RepScrubWQ
		 	void _process()
		 		PG *pg = osd->_lookup_lock_pg(msg->pgid);
		 		pg->replica_scrub(msg, handle);

		/*
		  Guessing:
		  	MOSDRepScrub or MSG_OSD_REP_SCRUB comes in scrubing process, to request replica to do scrubing
		*/

	5.5. where MOSDScrub msg comes from

		OSDMonitor::preprocess_command()		// handle cli commands
			...
			else if ((prefix == "osd scrub" || prefix == "osd deep-scrub" || prefix == "osd repair"))
				mon->try_send_message(new MOSDScrub(osdmap.get_fsid(), pvec.back() == "repair", pvec.back() == "deep-scrub"), osdmap.get_inst(osd));

		PGMonitor::preprocess_command(MMonCommand *m)		// handle cli commands
			...
			else if (prefix == "pg scrub" || prefix == "pg repair" || prefix == "pg deep-scrub") 
	     		mon->try_send_message(new MOSDScrub(mon->monmap->fsid, pgs, scrubop == "repair", scrubop == "deep-scrub"), mon->osdmon()->osdmap.get_inst(osd));

	    /*
	    	They come from user cli commands
	    */

6. OSD startup

	6.1. OSD booting

		[osd]
		OSD::start_boot()
			C_OSD_GetVersion *c = new C_OSD_GetVersion(this);
			monc->get_version("osdmap", &c->newest, &c->oldest, c);
				...
				C_OSD_GetVersion::finish()
					osd->_maybe_boot(oldest, newest);
						if (osdmap->test_flag(CEPH_OSDMAP_NOUP))
							log ...
						else if (is_waiting_for_healthy() || !_is_healthy())
							if (!is_waiting_for_healthy())
	      						start_waiting_for_healthy();
	      					heartbeat_kick();
	      				else if osdmap->get_epoch() >= oldest - 1 && osdmap->get_epoch() + cct->_conf->osd_map_message_max > newest
	      					_send_boot();
	      						MOSDBoot *mboot = new MOSDBoot(superblock, boot_epoch, hb_back_addr, hb_front_addr, cluster_addr);
	      						_collect_metadata(&mboot->metadata);
	      						monc->send_mon_message(mboot);
	      					return

	      				// get all the latest maps
	      				// subscribe后，将会得到Monitor发来的MOSDMap消息。MOSDMap消息Monitor和OSD都可以发。MOSDMap到handle_osd_map()中，又会触发start_boot()
						if (osdmap->get_epoch() > oldest)
							osdmap_subscribe(osdmap->get_epoch() + 1, true);
						else
							osdmap_subscribe(oldest - 1, true);
		/*
			start_boot()中，
				如果OSDMap版本够新，则
					monc->set_mon_message(MOSDBoot mboot)
					Monitor给MOSDMap消息，包含最新OSDMap
				如果不够，则
					osdmap_subscribe(...)
					Monitor发送OSD订阅的MOSDMap消息
					handle_osd_map(MOSDMap m)
						...
						start_boot()
					重新又绕回到start_boot()
		*/

		// after moc->send_mon_message(MOSDBoot mboot)
		[mon]
		PaxosService::dispatch()
			OSDMonitor::preprocess_query()
				preprocess_boot()
					// already booted?
					if (osdmap.is_up(from) && osdmap.get_inst(from) == m->get_orig_source_inst())
						_booted(m, false)
							send_latest(m, m->sb.current_epoch+1);
								if (start == 0)
									send_full(m);
										mon->send_reply(MOSDMap *m)
								else
									send_incremental(m, start);
										mon->send_reply(MOSDMap *m)
						return true
					// noup?
					if (!can_mark_up(from))
						send_latest(m, m->sb.current_epoch+1);
						return true

		// 最终从Monitor发回MOSDMap消息
		[osd]
		OSD::handle_osd_map(..)
			...
			state = STATE_ACTIVE
			...

	6.2. init processes

		// 无资源分配
		OSD::pre_init()
			cct->_conf->add_observer(this);

		OSD::init()
			store->mount();
			read_superblock();
				store->read(coll_t::META_COLL, OSD_SUPERBLOCK_POBJECT, 0, 0, bl);
				::decode(superblock, p);
			
			// make sure info object exists
			if (!store->exists(coll_t::META_COLL, service.infos_oid))
				t.touch(coll_t::META_COLL, service.infos_oid);
				r = store->apply_transaction(t);

			// make sure snap mapper object exists
			...

			// lookup "current" osdmap
			osdmap = get_map(superblock.current_epoch);
				return service.get_map(e);
					OSDMapRef ret(try_get_map(e));
						OSDService::try_get_map(epoch_t epoch)
							OSDMapRef retval = map_cache.lookup(epoch);
							if (retval)
								return retval
							OSDMap *map = new OSDMap;
							_get_map_bl(epoch, bl)
								 store->read(coll_t::META_COLL, OSD::get_osdmap_pobject_name(e), 0, 0, bl) >= 0;
							map->decode(bl);
							return _add_map(map);
								OSDMapRef l = map_cache.add(e, o);

			// load up pgs (as they previously existed)
  			load_pgs();
  				set<spg_t> head_pgs;
  				map<spg_t, interval_set<snapid_t> > pgs;
  				for (vector<coll_t>::iterator it = ls.begin(); it != ls.end(); ++it)
  					pgs[pgid].insert(snap);
  					head_pgs.insert(pgid);

  				bool has_upgraded = false;
  				for (map<spg_t, interval_set<snapid_t> >::iterator i = pgs.begin(); i != pgs.end(); ++i)
  					spg_t pgid(i->first);

  					epoch_t map_epoch = PG::peek_map_epoch(store, coll_t(pgid), service.infos_oid, &bl);
  					PG *pg = _open_lock_pg(map_epoch == 0 ? osdmap : service.get_map(map_epoch), pgid);
  						PG* pg = _make_pg(createmap, pgid);
  							PGPool pool = _get_pool(pgid.pool(), createmap);
  							pg = new ReplicatedPG(&service, createmap, pool, pgid, logoid, infooid);
  						pg->lock(no_lockdep_check);

  					// read pg state, log
    				pg->read_state(store, bl);

    				if (pg->must_upgrade())
    					has_upgraded = true;
    					pg->upgrade(store, i->second);

    				service.init_splits_between(pg->info.pgid, pg->get_osdmap(), osdmap);
    				pg->reg_next_scrub();

    				pg->get_osdmap()->pg_to_up_acting_osds(pgid.pgid, &up, &up_primary, &acting, &primary); 
			        pg->init_primary_up_acting(up, acting, up_primary, primary);

			        int role = OSDMap::calc_pg_role(whoami, pg->acting);
    				pg->set_role(role);

    				PG::RecoveryCtx rctx(0, 0, 0, 0, 0, 0);
    				pg->handle_loaded(&rctx);

    			build_past_intervals_parallel();

    		// i'm ready!
    		client_messenger->add_dispatcher_head(this);
  			...

  			service.init();		// OSDService::init()
			service.publish_map(osdmap);
			service.publish_superblock(superblock);

			consume_map();

			state = STATE_BOOTING;
  			start_boot();
  				to 6.1

  		OSD::final_init()
  			AdminSocket *admin_socket = cct->get_admin_socket();
  			test_ops_hook = new TestOpsSocketHook(&(this->service), this->store);

  			r = admin_socket->register_command(..)
  			... // init admin sockets

7. ObjectStore

	7.1. How ObjectStore finally calls LevelDB

		KeyValueStore::do_transactions(list<Transaction*> &tls, uint64_t op_seq)
			return _do_transactions(tls, op_seq, 0);
				for (list<Transaction*>::iterator p = tls.begin(); p != tls.end(); ++p, trans_num++)
					r = _do_transaction(**p, bt, spos, handle);
						...	// a lot of transaction op
				r = bt.submit_transaction();	// KeyValueStore::BufferTransaction::submit_transaction()
					r = store->backend->save_strip_header(header, spos, t);
					return store->backend->submit_transaction(t);	// store->backend is StripObjectMap
						return db->submit_transaction(t);	// GenericObjectMap::submit_transaction()
							// KeyValueDB::submit_transaction(), actually LevelDB::submit_transaction()
							leveldb::Status s = db->Write(leveldb::WriteOptions(), &(_t->bat)); 

8. MSG_OSD_PG_CREATE

	8.1 where it comes?

		/*
			这个函数在PGMonitor中经常性地被调用，基本上paxos一有变动就被调用
		*/
		PGMonitor::send_pg_creates()
			for (map<int, set<pg_t> >::iterator p = pg_map.creating_pgs_by_osd.begin()
			PGMonitor::send_pg_creates(int osd, Connection *con)
				...
				/* m.mkpg携带要创建什么PG， 它来自于PGMonitor::pg_map.creating_pgs_by_osd.find(osd)*/
				MOSDPGCreate *m = new MOSDPGCreate(mon->osdmon()->osdmap.get_epoch());
				...
	
	8.2 Handling PG creation
		OSD::handle_pg_create()
			MOSDPGCreate *m = (MOSDPGCreate*)op->get_req();
			for (map<pg_t,pg_create_t>::iterator p = m->mkpg.begin(); p != m->mkpg.end(); ++p)
				pg_t on = p->first;
				spg_t pgid;
				bool mapped = osdmap->get_primary_shard(on, &pgid);
				
				// register.
				creating_pgs[pgid].history = history;
				creating_pgs[pgid].parent = parent;
				creating_pgs[pgid].acting.swap(acting);
				
				PG *pg = NULL;
				if (can_create_pg(pgid))
					pg = _create_lock_pg(osdmap, pgid, true, false, false, 0, creating_pgs[pgid].acting, whoami, creating_pgs[pgid].acting, whoami,	history, pi, *rctx.transaction);
						PG *pg = _open_lock_pg(createmap, pgid, true, hold_map_lock);
							PG* pg = _make_pg(createmap, pgid);
								pg = new ReplicatedPG(&service, createmap, pool, pgid, logoid, infooid);
						service.init_splits_between(pgid, pg->get_osdmap(), service.get_osdmap());	
						pg->init(role, up, up_primary, acting, acting_primary, history, pi, backfill, &t);
						return pg;
					pg->handle_create(&rctx);
					pg->publish_stats_to_osd();
						// a lot of updating this.info
						...
						if (is_primary())
							osd->pg_stat_queue_enqueue(this);
				dispatch_context(rctx, pg, osdmap);
					do_notifies(*ctx.notify_list, curmap);
					do_queries(*ctx.query_map, curmap);
					do_infos(*ctx.info_map, curmap);
				
			maybe_update_heartbeat_peers();			
	
	8.3 PG::upgrade(..)
		PG::upgrade(..)
			for (interval_set<snapid_t>::const_iterator i = snapcolls.begin(); i != snapcolls.end(); ++i)
				for (snapid_t next_dir = i.get_start(); next_dir != i.get_start() + i.get_len(); ++next_dir)
					coll_t cid(info.pgid, next_dir);
					int r = get_pgbackend()->objects_list_partial(cur, store->get_ideal_list_min(), store->get_ideal_list_max(), 0, &objects, &cur);
					for (vector<hobject_t>::iterator j = objects.begin(); j != objects.end(); ++j)
						t.remove(cid, *j);
			
			while (1)
				/* to repair snap? */
				for (vector<hobject_t>::iterator j = objects.begin(); j != objects.end(); ++j)
					...
					snap_mapper.get_snaps(*j, &cur_snaps);
					...
					snap_mapper.add_oid(*j, oi_snaps, &_t);
			
9. MSG_OSD_PG_NOTIFY
	9.1 handle_pg_notify
		/** PGNotify
		 * from non-primary to primary
		 * includes pg_info_t.
		 * NOTE: called with opqueue active.
		 */
		 OSD::handle_pg_notify(..)
			handle_pg_peering_evt(..)
			/*
			 * look up a pg.  if we have it, great.  if not, consider creating it IF the pg mapping
			 * hasn't changed since the given epoch and we are the primary.
			 */
					PG *pg = _create_lock_pg(..)
	
	9.2. where it comes from
		
			OSD::handle_pg_query(OpRequestRef op) || OSD::dispatch_context(..)
				/** do_notifies
				 * Send an MOSDPGNotify to a primary, with a list of PGs that I have
				 * content for, and they are primary for.
				 */
				OSD::do_notifies(..)
					 MOSDPGNotify *m = new MOSDPGNotify(..)
					 
10. MSG_OSD_PG_QUERY
	10.1 handle_pg_query
		/** PGQuery
		 * from primary to replica | stray
		 * NOTE: called with opqueue active.
		 */
		OSD::handle_pg_query(..)
			pg->queue_query(..)
				...
				peering_queue.push_back(evt);
				to next
			...
			MOSDPGLog *mlog = new MOSDPGLog();
			_share_map_outgoing(from, con.get(), osdmap);
			cluster_messenger->send_message(mlog, con.get());
			...
			do_notifies(notify_list, osdmap);
		
		[after pg->queue_query]
			... // seems to be related to recovery process
	
	10.2 where PGQuery comes from
		OSD::dispatch_context
			OSD::do_queries(..)
				...
				
11. MSG_OSD_PG_LOG
	
	11.1 handle
		OSD::handle_pg_log(OpRequestRef op)
			handle_pg_peering_evt(..);
				...
				pg->queue_peering_event(evt);
				...
				
	11.2. where comes
		OSD::handle_pg_query(OpRequestRef op)
			...
		PG::activate(..)
			...
		PG::share_pg_log()
			...
		PG::fulfill_log(..)
			...
	
12. MSG_OSD_PG_INFO
		OSD::handle_pg_info(OpRequestRef op)
			handle_pg_peering_evt(..)
		
		/* where comes */
		OSD::dispatch_context(..)
			do_infos(..)
		PG::share_pg_info(..)
			...
		PG::PG::_activate_committed(epoch_t e)
			...

13. MSG_OSD_PG_SCAN
	
	13.1 where it comes?
		ReplicatedPG::do_scan(..)
		ReplicatedPG::recover_backfill(..)

	13.2. handle_pg_scan
		OSD::handle_pg_scan(..)
			pg = _lookup_pg(m->pgid);
			enqueue_op(pg, op);
				pg->queue_op(op);
					osd->op_wq.queue(make_pair(PGRef(this), op));

		[OSD::OpWQ]
		OSD::OpWQ::_process(..)
			osd->dequeue_op(pg, op, handle);
				op->mark_reached_pg();
				pg->do_request(op, handle);
					ReplicatedPG::do_request(..)
						case MSG_OSD_PG_SCAN:
    						do_scan(op, handle);
    							...
    							MOSDPGScan *reply = new MOSDPGScan(..)
    							...
    							/*
    								Seems heavily related to Backfill. From http://ceph.com/docs/master/rados/operations/pg-states/ see:
    								Backfill
										Ceph is scanning and synchronizing the entire contents of a placement group instead of inferring what contents need to be synchronized from the logs of recent operations. Backfill is a special case of recovery.
    							*/

14. what is CephPeeringEvt?
	14.1. PG.h::class CephPeeringEvt{
			epoch_sent, epoch_requested, 
			evt,
		}
	     no subclasses

	14.2. PG::queue_peering_event(CephPeeringEvtRef evt)
			peering_queue.push_back(evt);
			OSDService::queue_for_peering(PG *pg=this)
				peering_wq.queue(pg);

		  OSD::peering_wq::_process(..)
		  	osd->process_peering_events(pgs, handle);
		  		for (list<PG*>::const_iterator i = pgs.begin(); i != pgs.end(); ++i) {
		  			advance_pg(curmap->get_epoch(), pg, handle, &rctx, &split_pgs);

		  			PG::CephPeeringEvtRef evt = pg->peering_queue.front();
		  			pg->handle_peering_event(evt, &rctx);
		  				recovery_state.handle_event(evt, rctx);

		  			pg->write_if_dirty(*rctx.transaction);
		  		}

15. CephPeeringEvent and Recovery
    Ceph peering model: http://lists.ceph.com/pipermail/ceph-users-ceph.com/attachments/20130415/39f25f5a/attachment-0001.png

	// general pg op process
	enqueue
	_process
	dequeue
	op->mark_reached_pg();
	pg->do_request(op, handle);

	// pg scan
	PGBackend::objects_list_partial(..)
			ObjectStore::collection_list_partial()
				KeyValueStore
					StripObjectMap
						GenericObjectMap::list_objects(..)
							KeyValueDB::get_iterator()

	// ----------------

	// queue_peering_event(CephPeeringEvent..)

	PG::queue_peering_event(CephPeeringEvtRef evt)
		peering_queue.push_back(evt);
		osd->queue_for_peering(this);

	OSD::peering_wq::_process()
		osd->process_peering_events(pgs, handle);
			advance_pg(curmap->get_epoch(), pg, handle, &rctx, &split_pgs);
				pg->handle_advance_map(nextmap, lastmap, newup, up_primary, newacting, acting_primary, rctx);
					recovery_state.handle_event(evt, rctx);
				if (parent.is_split(..))
					.. // handle splits
			
			PG::CephPeeringEvtRef evt = pg->peering_queue.front();
			pg->peering_queue.pop_front();
			pg->handle_peering_event(evt, &rctx);
				recovery_state.handle_event(evt, rctx);
			
			pg->write_if_dirty(*rctx.transaction);
			
	// PG recover states

	Initial 
		Load -> Reset
		MNotifyRec -> Primary
		MInfoRec -> Stray
		MLogRec -> Stray
		
	Started
		AdvMap -> (up or acting affected)?Reset:Nothing

	Reset
		AdvMap -> 
			 pg->start_peering_interval(..)
				 init_primary_up_acting(..)
				 // did acting, up, primary|acker change?
				 ...
				 // did primary change?
				 ...
		ActMap -> Started
		
	Primary
		NeedActingChange -> WaitActingChange
		
	Peering
		pg->state_set(PG_STATE_PEERING);
		
		Activate -> Active
		AdvMap -> Reset
		
	Backfilling
		pg->osd->queue_for_recovery(pg);

		RemoteReservationRejected 
			pg->osd->local_reserver.cancel_reservation(pg->info.pgid);
			pg->state_set(PG_STATE_BACKFILL_TOOFULL);
			-> NotBackfilling
		Backfilled -> Recovered
		
	WaitRemoteBackfillReserved
		RemoteReservationRejected
		AllBackfillsReserved -> Backfilling
		RemoteBackfillReserved -> 
			if(){
				if(){
					pg->osd->send_message_osd_cluster(new MBackfillReserve(..)..)
				}else{
					post_event(RemoteBackfillReserved());
				}
			}else{
				post_event(AllBackfillsReserved());
			}

	WaitLocalBackfillReserved
		LocalBackfillReserved -> WaitRemoteBackfillReserved

	NotBackfilling & Activating
		RequestBackfill -> WaitLocalBackfillReserved
		

	Active
		AdvMap -> 
		ActMap ->
		MNotifyRec -> 
		MInfoRec -> 
		MLogRec -> 
		AllReplicasActivated -> 

	Activating
		AllReplicasRecovered, Recovered
		DoRecovery, WaitLocalRecoveryReserved
		RequestBackfill, WaitLocalBackfillReserved

	ReplicaActive

	Stray

	Recovering
		pg->osd->queue_for_recovery(pg);

		AllReplicasRecovered -> Recovered
		RequestBackfill -> WaitRemoteBackfillReserved

	WaitRemoteRecoveryReserved
		RemoteRecoveryReserved -> 
		AllRemotesReserved -> Recovering

	WaitLocalRecoveryReserved
		LocalRecoveryReserved -> WaitRemoteRecoveryReserved

	Clean & Activating
		DoRecovery -> WaitLocalRecoveryReserved
		
	Clean
		DoRecovery -> WaitLocalRecoveryReserved
		
	-------
	pg->osd->queue_for_recovery(pg);
		OSD::do_recovery(PG *pg, ThreadPool::TPHandle &handle)
			bool more = pg->start_recovery_ops(max, &rctx, handle, &started);
				ReplicatedPG::start_recovery_ops(..)
					recover_replicas(..)
						started += prep_object_replica_pushes(soid, r->second.need, h);
						pgbackend->run_recovery_op(h, cct->_conf->osd_recovery_op_priority)

					recover_primary(..)
						pgbackend->run_recovery_op(h, cct->_conf->osd_recovery_op_priority);
					
					recover_backfill(..)

					if started < max
						RequestBackfill()   // so, backfill is a special case for recoverying, when normal reovery cannot succeed
						
	------

	/*
		according to https://github.com/ceph/ceph/blob/master/doc/dev/osd_internals/recovery_reservation.rst
		there are two kinds of recovery: log-based recovery and backfill
		recover_replica() & recover_primary() try to do log-based recovery
		recover_backfill() does backfill recovery.
		backfill is to copy all objects instead of log
	*/

	//TODO PG:Activate() read and get to know recovery/backfill

	//TOOD how snap works, snapmanager
					
16. OSD Scrubbing
    "Silent data corruption caused by hardware can be a big issue on a large data store. RADOS offers a scrubbing feature" 
    
    "Regular scrubbing is lighter and checks that the object is correctly replicated among the nodes. It also checks the object’s metadata and attributes. Deep scrubbing is heavier and expands the check to the actual data."

    "It ensures data integrity by reading the data and computing checksums."
    	-- https://www.usenix.org/system/files/login/articles/02_giannakos.pdf

   	in swift, the same thing is done by "Auditor"

    	// register scrubbing
    	pg->reg_next_scrub();
    		osd->reg_last_pg_scrub(info.pgid, scrubber.scrub_reg_stamp);

    	// schedule scrubbing
    	OSD::tick()
    		OSD::sched_scrub();
    			PG::sched_scrub()
    				queue_scrub();
    					state_set(PG_STATE_SCRUBBING);
    					osd->queue_for_scrub(this)

    	// do scrubbing
    	OSD::ScrubWQ::_process()
			pg->scrub(handle);
				if (scrubber.is_chunky) {
					chunky_scrub(handle);
						while (!done) {
							switch (scrubber.state) {
      							case PG::Scrubber::INACTIVE:
      								scrubber.state = PG::Scrubber::NEW_CHUNK;
      							case PG::Scrubber::NEW_CHUNK:
      							...
      							...
      							case PG::Scrubber::COMPARE_MAPS:
      							case PG::Scrubber::FINISH:
      						}
						}
				} else {
					classic_scrub(handle);
						...
				}

17. PGBackend::objects_list_partial()
		ObjectStore::collection_list_partial()
    PGBackend::objects_list_range()
    	ObjectStore::collection_list_range()

    ObjectStore::collection_list_partial()
    ObjectStore::collection_list_range()

    ObjectStore::get_ideal_list_min()
    ObjectStore::get_ideal_list_max()

    	@see ObjectStore.h, detailed comments

18. PG startup process
		PG::PG() 
			... // do nothing

		PG::init()
			... // set role, actiing set
		
		PG::activate()
			state_set(PG_STATE_ACTIVE);
			... // log, recovery, backfill stuff

19. snap mechanism & io path
    http://ceph.com/docs/master/dev/osd_internals/snaps/
    http://www.wzxue.com/%E8%A7%A3%E6%9E%90ceph-snapshot/
    http://blog.sina.com.cn/s/blog_c2e1a9c7010151xb.html
	
	/* 收到client op */
	OSD::dispatch_op()
		case CEPH_MSG_OSD_OP:
			handle_op(op);
				MOSDOp *m = static_cast<MOSDOp*>(op->get_req());
				/*
					MOSDOp中
						snapid_t snapid;
						snapid_t snap_seq;
					与snapshot有关
				*/
				enqueue_op(pg, op);
					PG::queue_op(OpRequestRef op)
						osd->op_wq.queue(make_pair(PGRef(this), op));
	
	/* 进入处理 */
	OSD::OpWQ::_process()
		osd->dequeue_op(pg, op, handle);
			pg->do_request(op, handle);
				ReplicatedPG::do_request(OpRequestRef op, ThreadPool::TPHandle &handle)
					case CEPH_MSG_OSD_OP:
						ReplicatedPG::do_op(op)
							if (op->includes_pg_op()) {
								return do_pg_op(op);
							}
							
							hobject_t head(m->get_oid(), m->get_object_locator().key,
								CEPH_NOSNAP, m->get_pg().ps(),
								info.pgid.pool(), m->get_object_locator().nspace);
							hobject_t snapdir(m->get_oid(), m->get_object_locator().key,
								CEPH_SNAPDIR, m->get_pg().ps(), info.pgid.pool(),
								m->get_object_locator().nspace);
							
							ObjectContextRef obc;		
							hobject_t oid(m->get_oid(),
								m->get_object_locator().key,
								m->get_snapid(),
								m->get_pg().ps(),
								m->get_object_locator().get_pool(),
								m->get_object_locator().nspace);
							r = find_object_context(oid, &obc, can_create, &missing_oid);
							
							map<hobject_t,ObjectContextRef> src_obc;
							for (vector<OSDOp>::iterator p = m->ops.begin(); p != m->ops.end(); ++p) {
								hobject_t src_oid(osd_op.soid, src_oloc.key, m->get_pg().ps(),
									info.pgid.pool(), m->get_object_locator().nspace);
								r = find_object_context(src_oid, &sobc, false, &wait_oid)
								src_obc[src_oid] = sobc;
							}
							
							 // any SNAPDIR op needs to have all clones present.
							if (m->get_snapid() == CEPH_SNAPDIR){
								for (vector<snapid_t>::iterator p = obc->ssc->snapset.clones.begin(); p != obc->ssc->snapset.clones.end(); ++p) {
									hobject_t clone_oid = obc->obs.oi.soid;
									clone_oid.snap = *p;
									if (!src_obc.count(clone_oid)){
										ObjectContextRef sobc;
										r = find_object_context(clone_oid, &sobc, false, &wait_oid);
										src_obc[clone_oid] = sobc;
									}
								}
							}
							
							OpContext *ctx = new OpContext(op, m->get_reqid(), m->ops,
											&obc->obs, obc->ssc, 
											this);
							ctx->op_t = pgbackend->get_transaction();
							ctx->obc = obc;
							
							ctx->src_obc = src_obc;
							execute_ctx(ctx);
								/* this method must be idempotent since we may call it several times
  								   before we finally apply the resulting transaction. */
								if (op->may_write() || op->may_cache()) {
									 // snap
									if (pool.info.is_pool_snaps_mode()) {
										// use pool's snapc
										ctx->snapc = pool.snapc;
									}else{
										// client specified snapc
										ctx->snapc.seq = m->get_snap_seq();
										ctx->snapc.snaps = m->get_snaps();
									}
								}
								
								int result = prepare_transaction(ctx);
									const hobject_t& soid = ctx->obs->oi.soid;
									int result = do_osd_ops(ctx, ctx->ops);
										PGBackend::PGTransaction* t = ctx->op_t;
										for (vector<OSDOp>::iterator p = ops.begin(); p != ops.end(); ++p, ctx->current_osd_subop_num++) {
											// the greate swtich-case where op is handled
											switch (op.op) {
												case CEPH_OSD_OP_WATCH:
												...
												case CEPH_OSD_OP_READ:
													int r = pgbackend->objects_read_sync(
															soid, op.extent.offset, op.extent.length, &osd_op.outdata);
												case CEPH_OSD_OP_LIST_SNAPS:
													obj_list_snap_response_t resp;
													resp.clones.reserve(clonecount);
													resp.clones.push_back(ci);
													resp.encode(osd_op.outdata);
												case CEPH_OSD_OP_WRITE:
													t->write(soid, op.extent.offset, op.extent.length, osd_op.indata);
												...
												case ...
												...
												case ...
												...
												case ...								
												...
												case ...
												...
												...





												/* 
													the great switch-case 
												*/





												case ...
												...
											}
										}
										
									do_osd_op_effects(ctx);
										... // notify/callbacks
									
									// clone, if necessary
									if (soid.snap == CEPH_NOSNAP)
										make_writeable(ctx);
											const hobject_t& soid = ctx->obs->oi.soid;
											PGBackend::PGTransaction *t = pgbackend->get_transaction();
											hobject_t coid = soid;
											coid.snap = snapc.seq;
											
											ctx->clone_obc = object_contexts.lookup_or_create(static_snap_oi.soid);
											ctx->clone_obc->destructor_callback = new C_PG_ObjectContext(this, ctx->clone_obc.get());
											ctx->clone_obc->obs.oi = static_snap_oi;
											ctx->clone_obc->obs.exists = true;
											
											_make_clone(ctx, t, ctx->clone_obc, soid, coid, snap_oi);
												t->clone(head, coid);
												
											// prepend transaction to op_t
											t->append(ctx->op_t);
											delete ctx->op_t;
											ctx->op_t = t;
									
									finish_ctx(ctx,	ctx->new_obs.exists ? pg_log_entry_t::MODIFY : pg_log_entry_t::DELETE);
										// snapset
										if (soid.snap == CEPH_NOSNAP) {
											hobject_t snapoid(soid.oid, soid.get_key(), CEPH_SNAPDIR, soid.hash, info.pgid.pool(), soid.get_namespace());

											ctx->op_t->stash(snapoid, ctx->at_version.version);
										}

										if (ctx->new_obs.exists) {
											bufferlist bv(sizeof(ctx->new_obs.oi));
										    ::encode(ctx->new_obs.oi, bv);
										    setattr_maybe_cache(ctx->obc, ctx, ctx->op_t, OI_ATTR, bv);
										}

								bool successful_write = !ctx->op_t->empty() && op->may_write() && result >= 0;
								
								// issue replica writes
								RepGather *repop = new_repop(ctx, obc, rep_tid);
								repop->src_obc.swap(src_obc);
								
								issue_repop(repop, now);
									pgbackend->submit_transaction(
									    soid,
									    repop->ctx->at_version,
									    repop->ctx->op_t,
									    pg_trim_to,
									    repop->ctx->log,
									    onapplied_sync,
									    on_all_applied,
									    on_all_commit,
									    repop->rep_tid,
									    repop->ctx->reqid,
									    repop->ctx->op);
									    	RPGTransaction *t = dynamic_cast<RPGTransaction*>(_t);
									    	
									    	issue_op(      // ReplicatedBackend::issue_op
											    soid,
											    at_version,
											    tid,
											    reqid,
											    trim_to,
											    t->get_temp_added().size() ? *(t->get_temp_added().begin()) : hobject_t(),
											    t->get_temp_cleared().size() ?
											      *(t->get_temp_cleared().begin()) :hobject_t(),
											    log_entries,
											    &op,
											    op_t);

											    /* 各个replica接到数据是在这里 */
											    for (set<pg_shard_t>::const_iterator i = parent->get_actingbackfill_shards().begin(); i != parent->get_actingbackfill_shards().end(); ++i) {
												    // forward the write/update/whatever
												    MOSDSubOp *wr = new MOSDSubOp(
												      reqid, parent->whoami_shard(),
												      spg_t(get_info().pgid.pgid, i->shard),
												      soid,
												      false, acks_wanted,
												      get_osdmap()->get_epoch(),
												      tid, at_version);

												    // ship resulting transaction, log entries, and pg_stats
												    ::encode(*op_t, wr->get_data());
												    get_parent()->send_message_osd_cluster(peer.osd, wr, get_osdmap()->get_epoch());
												}
											
											/* op写入本地是在这里 */
											parent->queue_transaction(op_t, op.op);
												ReplicatedPG::queue_transaction(ObjectStore::Transaction *t, OpRequestRef op)
												osd->store->queue_transaction(osr.get(), t, 0, 0, 0, op);
								
								/* 主要是，send ack */
								eval_repop(repop);
									MOSDOp *m = NULL;
									m = static_cast<MOSDOp *>(repop->ctx->op->get_req());

									// send commit.
									MOSDOpReply *reply = repop->ctx->reply;
									osd->send_message_osd_client(reply, m->get_connection());

									// applied?
									for (list<OpRequestRef>::iterator i = waiting_for_ack[repop->v].begin(); i != waiting_for_ack[repop->v].end(); ++i) {
										MOSDOpReply *reply = new MOSDOpReply(m, 0, get_osdmap()->get_epoch(), 0, true);
										osd->send_message_osd_client(reply, m->get_connection());
									}

									// done.
									if (repop->all_applied && repop->all_committed) {
										repop_queue.pop_front();
    									remove_repop(repop);
									}

	/* replica收到MOSDSubOp */
	OSD::dispatch_op(..)
		case CEPH_MSG_OSD_OP:
    		handle_op(op);
    			enqueue_op(pg, op);
    				 pg->queue_op(op);
    				 	osd->op_wq.queue(make_pair(PGRef(this), op));

    OSD::OpWQ::_process(..)
    	osd->dequeue_op(pg, op, handle);
    		pg->do_request(op, handle);
    			ReplicatedPG::do_request(..)
    				pgbackend->handle_message(op)
    					case MSG_OSD_SUBOP:
    						OSDOp *first = &m->ops[0];
							switch (first->op.op) {
								case CEPH_OSD_OP_PULL:
									sub_op_pull(op);
									return true;
								case CEPH_OSD_OP_PUSH:
									sub_op_push(op);
										handle_push(m->from, pop, &resp, t);
											submit_push_data(pop.recovery_info,
											   first,
											   complete,
											   pop.data_included,
											   data,
											   pop.omap_header,
											   pop.attrset,
											   pop.omap_entries,
											   t);
											   		... // many operations are written into t
											   		submit_push_complete(recovery_info, t);
										get_parent()->queue_transaction(t);
									return true
							}
							sub_op_modify(op);
								RepModifyRef rm(new RepModify);
								...
								parent->queue_transaction(&(rm->localt), op);

    				case MSG_OSD_SUBOP:
    					do_sub_op(op);
    						... // 这个是给scrubber用的
    					break;


19.5 ondisk object structure
	1. object_t
	   snapid_t

	   sobject_t = object_t + snapid_t (snapped object)
	   hobject_t = object_t + snapid_t + hash (hashed object)
	   ghobject_t = hobject_t + gen_t + shard_t (generationed object)
	   		gen_t = version_t
	   		shard_t = uint8_t

	   coll_t = str (collection)
	   
	   pg_t = m_pool
	   spg_t = shard_id_t + pg_t
	   pg_t => spg_t : OSDMap::get_primary_shard(pg_t, spg_t){
						*out = spg_t(pgid);}		// NO_SHARD

```

Ceph OSD structure chart

![Ceph OSD Structure](/images/ceph-osd-structure.png "Ceph OSD Structure")

OSD PG (Placement Group) peering states chart

![PG Peering States](/images/ceph-pg-peering-states.png "PG Peering States")

