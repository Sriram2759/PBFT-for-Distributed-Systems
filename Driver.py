# -*- generated by 1.0.12 -*-
import da
PatternExpr_481 = da.pat.TuplePattern([da.pat.ConstantPattern('done')])
PatternExpr_486 = da.pat.BoundPattern('_BoundPattern487_')
PatternExpr_521 = da.pat.TuplePattern([da.pat.ConstantPattern('done')])
PatternExpr_526 = da.pat.BoundPattern('_BoundPattern527_')
PatternExpr_556 = da.pat.TuplePattern([da.pat.ConstantPattern('Test-done')])
PatternExpr_561 = da.pat.BoundPattern('_BoundPattern562_')
PatternExpr_694 = da.pat.TuplePattern([da.pat.ConstantPattern('Test-done'), da.pat.FreePattern('is_syystem_safe'), da.pat.FreePattern('is_system_live'), da.pat.FreePattern('totalmessagesinvolved'), da.pat.FreePattern('view_changed_happened')])
PatternExpr_729 = da.pat.TuplePattern([da.pat.ConstantPattern('Stats'), da.pat.FreePattern('avgproctime'), da.pat.FreePattern('walltime')])
PatternExpr_488 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.BoundPattern('_BoundPattern494_')]), da.pat.TuplePattern([da.pat.ConstantPattern('done')])])
PatternExpr_528 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.BoundPattern('_BoundPattern534_')]), da.pat.TuplePattern([da.pat.ConstantPattern('done')])])
PatternExpr_563 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.BoundPattern('_BoundPattern569_')]), da.pat.TuplePattern([da.pat.ConstantPattern('Test-done')])])
PatternExpr_888 = da.pat.TuplePattern([da.pat.ConstantPattern('done')])
PatternExpr_893 = da.pat.BoundPattern('_BoundPattern894_')
PatternExpr_895 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.BoundPattern('_BoundPattern901_')]), da.pat.TuplePattern([da.pat.ConstantPattern('done')])])
_config_object = {'channnel': 'fifo', 'clock': 'lamport'}
import sys
import sys
import time
import random
import hashlib
import csv
import os
import psutil
client_module = da.import_da('Client')
replica_module = da.import_da('Replica')
test_module = da.import_da('Test')
controller_module = da.import_da('controller')

class Driver(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._DriverReceivedEvent_0 = []
        self._DriverReceivedEvent_1 = []
        self._DriverReceivedEvent_2 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_DriverReceivedEvent_0', PatternExpr_481, sources=[PatternExpr_486], destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DriverReceivedEvent_1', PatternExpr_521, sources=[PatternExpr_526], destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DriverReceivedEvent_2', PatternExpr_556, sources=[PatternExpr_561], destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DriverReceivedEvent_3', PatternExpr_694, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Driver_handler_693]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DriverReceivedEvent_4', PatternExpr_729, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Driver_handler_728])])

    def setup(self, numReplica, numClients, numops, timeout, netwrkdelay, replicadelay, simulate_byzantine, **rest_907):
        super().setup(numReplica=numReplica, numClients=numClients, numops=numops, timeout=timeout, netwrkdelay=netwrkdelay, replicadelay=replicadelay, simulate_byzantine=simulate_byzantine, **rest_907)
        self._state.numReplica = numReplica
        self._state.numClients = numClients
        self._state.numops = numops
        self._state.timeout = timeout
        self._state.netwrkdelay = netwrkdelay
        self._state.replicadelay = replicadelay
        self._state.simulate_byzantine = simulate_byzantine
        self._state.nreplicas = self._state.numReplica
        self._state.nclients = self._state.numClients
        self._state.nops = self._state.numops
        self._state.tout = self._state.timeout
        self._state.ndelay = self._state.netwrkdelay
        self._state.rdelay = self._state.replicadelay
        self._state.is_syystem_safe = ''
        self._state.is_system_live = ''
        self._state.totalreplicamsgs = 0
        self._state.averageprocesstime = 0.0
        self._state.wallclocktime = 0.0
        self._state.view_changed_happened = ''
        self._state.rss_memory_percent = 0
        self._state.simulate_byzantine = self._state.simulate_byzantine

    def run(self):
        test_agent = self.new(test_module.Test, num=1)
        replicas = list(self.new(replica_module.Replica, num=self._state.nreplicas))
        maxfaultnum = int(((self._state.nreplicas - 1) / 3))
        if (self._state.simulate_byzantine == 2):
            byzantineset = list(random.sample(replicas, maxfaultnum))
            if (replicas[0] in byzantineset):
                byzantineset.remove(replicas[0])
        if (self._state.simulate_byzantine == 1):
            byzantineset = []
            if (maxfaultnum > 0):
                byzantineset = list(random.sample(replicas[1:], (maxfaultnum - 1)))
            byzantineset.append(replicas[0])
        if (self._state.simulate_byzantine == 0):
            byzantineset = set()
        self.output(byzantineset)
        self._setup(test_agent, (self._state.nclients, self._state.nreplicas, byzantineset))
        self._start(test_agent)
        initial_state = []
        ctl = self.new(controller_module.Controller, num=1)
        self._setup(ctl, ((self._state.nreplicas + self._state.nclients),))
        self._start(ctl)
        self._setup(replicas, (ctl, replicas, initial_state, 0, byzantineset, maxfaultnum, self._state.ndelay, self._state.rdelay, self._state.tout, test_agent))
        clients = self.new(client_module.Client, (ctl, replicas, self._state.nops, self._state.tout, 0, maxfaultnum, self._state.ndelay, test_agent), num=self._state.nclients)
        start_etime = time.time()
        self._start(replicas)
        start_ctime = time.time()
        self._start(clients)
        super()._label('_st_label_472', block=False)
        c = None

        def UniversalOpExpr_473():
            nonlocal c
            for c in clients:
                if (not PatternExpr_488.match_iter(self._DriverReceivedEvent_0, _BoundPattern494_=c, SELF_ID=self._id)):
                    return False
            return True
        _st_label_472 = 0
        while (_st_label_472 == 0):
            _st_label_472 += 1
            if UniversalOpExpr_473():
                _st_label_472 += 1
            else:
                super()._label('_st_label_472', block=True)
                _st_label_472 -= 1
        self.output('All clients done.')
        end_ctime = time.time()
        self.send(('done',), to=replicas)
        super()._label('_st_label_512', block=False)
        r = None

        def UniversalOpExpr_513():
            nonlocal r
            for r in replicas:
                if (not PatternExpr_528.match_iter(self._DriverReceivedEvent_1, _BoundPattern534_=r, SELF_ID=self._id)):
                    return False
            return True
        _st_label_512 = 0
        while (_st_label_512 == 0):
            _st_label_512 += 1
            if UniversalOpExpr_513():
                _st_label_512 += 1
            else:
                super()._label('_st_label_512', block=True)
                _st_label_512 -= 1
        self.output('All Replicas done.')
        end_etime = time.time()
        super()._label('_st_label_547', block=False)
        t = None

        def UniversalOpExpr_548():
            nonlocal t
            for t in test_agent:
                if (not PatternExpr_563.match_iter(self._DriverReceivedEvent_2, _BoundPattern569_=t, SELF_ID=self._id)):
                    return False
            return True
        _st_label_547 = 0
        while (_st_label_547 == 0):
            _st_label_547 += 1
            if UniversalOpExpr_548():
                _st_label_547 += 1
            else:
                super()._label('_st_label_547', block=True)
                _st_label_547 -= 1
        self.output('Test Module Done')
        Throughput = ((self._state.nclients * self._state.nops) / (end_ctime - start_ctime))
        TotalRunTime = (end_etime - start_etime)
        self.output('statistics', self._state.nclients, self._state.nreplicas, self._state.nops)
        self.output('statistics', self._state.ndelay, self._state.rdelay, byzantineset)
        self.output('statistics', Throughput, self._state.is_syystem_safe, self._state.is_system_live, (end_etime - start_etime), self._state.totalreplicamsgs, self._state.view_changed_happened)
        self.output('statistics', self._state.wallclocktime, self._state.averageprocesstime)
        process = psutil.Process(os.getpid())
        self._state.rss_memory_percent = process.memory_percent(memtype='rss')
        print('statistics', self._state.rss_memory_percent)
        self.output(self._id, self.parent())
        row = [self._state.nreplicas, self._state.nclients, self._state.nops, self._state.ndelay, self._state.rdelay, len(byzantineset), (replicas[0] in byzantineset), self._state.view_changed_happened, Throughput, TotalRunTime, self._state.wallclocktime, self._state.averageprocesstime, self._state.is_syystem_safe, self._state.is_system_live, self._state.totalreplicamsgs, self._state.rss_memory_percent]
        with open('Performance.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()
        self.send(('done',), to=self.parent())

    def _Driver_handler_693(self, is_syystem_safe, is_system_live, totalmessagesinvolved, view_changed_happened):
        self._state.is_syystem_safe = is_syystem_safe
        self._state.is_system_live = is_system_live
        self._state.view_changed_happened = view_changed_happened
        self._state.totalreplicamsgs = totalmessagesinvolved
    _Driver_handler_693._labels = None
    _Driver_handler_693._notlabels = None

    def _Driver_handler_728(self, avgproctime, walltime):
        self._state.averageprocesstime = float(avgproctime)
        self._state.wallclocktime = float(walltime)
    _Driver_handler_728._labels = None
    _Driver_handler_728._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._Node_ReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_Node_ReceivedEvent_0', PatternExpr_888, sources=[PatternExpr_893], destinations=None, timestamps=None, record_history=True, handlers=[])])

    def run(self):
        nreplicas = (int(sys.argv[1]) if (len(sys.argv) > 1) else 4)
        nclients = (int(sys.argv[2]) if (len(sys.argv) > 2) else 1)
        nops = (int(sys.argv[3]) if (len(sys.argv) > 3) else 2)
        timeout = (int(sys.argv[4]) if (len(sys.argv) > 4) else 10)
        netwrkdelay = (float(sys.argv[5]) if (len(sys.argv) > 5) else 0)
        replicadelay = (int(sys.argv[6]) if (len(sys.argv) > 6) else 0)
        simulate_byzantine = (int(sys.argv[7]) if (len(sys.argv) > 7) else 2)
        driver = self.new(Driver, [nreplicas, nclients, nops, timeout, netwrkdelay, replicadelay, simulate_byzantine])
        self._start(driver)
        super()._label('_st_label_885', block=False)
        _st_label_885 = 0
        while (_st_label_885 == 0):
            _st_label_885 += 1
            if PatternExpr_895.match_iter(self._Node_ReceivedEvent_0, _BoundPattern901_=driver):
                _st_label_885 += 1
            else:
                super()._label('_st_label_885', block=True)
                _st_label_885 -= 1
        self.output('Terminating Driver')