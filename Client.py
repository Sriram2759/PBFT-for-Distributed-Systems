# -*- generated by 1.0.12 -*-
import da
PatternExpr_432 = da.pat.TuplePattern([da.pat.ConstantPattern('REPLY'), da.pat.FreePattern('v'), da.pat.FreePattern('t'), da.pat.FreePattern('i'), da.pat.FreePattern('command_id'), da.pat.FreePattern('r')])
PatternExpr_472 = da.pat.TuplePattern([da.pat.ConstantPattern('REPLY'), da.pat.BoundPattern('_BoundPattern475_'), da.pat.BoundPattern('_BoundPattern476_'), da.pat.FreePattern(None), da.pat.BoundPattern('_BoundPattern478_'), da.pat.BoundPattern('_BoundPattern479_')])
PatternExpr_482 = da.pat.FreePattern('a')
_config_object = {'channnel': 'fifo', 'clock': 'lamport'}
import sys
sys.setrecursionlimit(100000)
import time
import random
import hashlib
controller_module = da.import_da('controller')
NOPS = 4

class Client(controller_module.Controllee, da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._ClientReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_0', PatternExpr_432, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_431]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_1', PatternExpr_472, sources=[PatternExpr_482], destinations=None, timestamps=None, record_history=True, handlers=[])])

    def setup(self, ctl, replicas, nops, timeout, current_view, maxfaultnum, ndelay, test_agent, **rest_580):
        super().setup(ctl=ctl, replicas=replicas, nops=nops, timeout=timeout, current_view=current_view, maxfaultnum=maxfaultnum, ndelay=ndelay, test_agent=test_agent, **rest_580)
        self._state.ctl = ctl
        self._state.replicas = replicas
        self._state.nops = nops
        self._state.timeout = timeout
        self._state.current_view = current_view
        self._state.maxfaultnum = maxfaultnum
        self._state.ndelay = ndelay
        self._state.test_agent = test_agent
        super().setup(self._state.ctl)
        self._state.cid = 0
        self._state.results = dict()
        self._state.count = dict()
        self._state.timeout_value = (3 * self._state.timeout)
        self._state.current_view = self._state.current_view
        self._state.clockValue = (- 1)
        self._state.resultlog = set()
        self._state.netwrkdelay = self._state.ndelay
        self._state.validresult = (- 999999999999999999999999)
        self._state.resultlog = set()
        self._state.primaryreplica = self._state.replicas[self._state.current_view]
        self._state.num_retries = 5

    @controller_module.run
    def run(self):
        self.sendrequest()
        self.output('Client Terminating')
        self.send(('done',), to=self.parent())

    def getMaxTorelentNumber(self):
        return self._state.maxfaultnum

    def sendrequest(self):
        for i in range(self._state.nops):
            self._state.resultlog.clear()
            self._state.clockValue = self.logical_clock()
            time.sleep(self._state.netwrkdelay)
            opno = random.randint(1, NOPS)
            arg1 = random.randint(1, 10)
            arg2 = random.randint(1, 10)
            self._state.cid += 1
            self.output('sending my request to ', self._state.primaryreplica)
            self.send(('REQUEST', (self._id, (opno, arg1, arg2), self._state.clockValue, self._state.cid)), to=self._state.primaryreplica)
            itr = 0
            while (itr < self._state.num_retries):
                super()._label('_st_label_382', block=False)
                _st_label_382 = 0
                self._timer_start()
                while (_st_label_382 == 0):
                    _st_label_382 += 1
                    if (self._state.cid in self._state.results):
                        self.output('The result received for request no ', i, ' is ', self._state.results[self._state.cid])
                        break
                        _st_label_382 += 1
                    elif self._timer_expired:
                        self.output('I am client and brodcasting again', opno, arg1, arg2)
                        time.sleep(self._state.netwrkdelay)
                        self.send(('REQUEST', (self._id, (opno, arg1, arg2), self._state.clockValue, self._state.cid)), to=self._state.replicas)
                        _st_label_382 += 1
                    else:
                        super()._label('_st_label_382', block=True, timeout=self._state.timeout_value)
                        _st_label_382 -= 1
                else:
                    if (_st_label_382 != 2):
                        continue
                if (_st_label_382 != 2):
                    break
                itr += 1
            if (itr == 3):
                self.output('Failed to perform operation')

    def send_liveness_result(self, pv, nv):
        self.send(('Liveness', pv, nv, self._id), to=self._state.test_agent)

    def _Client_handler_431(self, v, t, i, command_id, r):
        f = self.getMaxTorelentNumber()
        self._state.resultlog.add(('REPLY', v, t, i, self._state.cid, str(r)))
        '\n\t\tThe client waits for f+1 replies with valid signatures from different replicas,\n\t\tand with the same t and r, before accepting the result r. \n\t\tThis ensures that the result is valid, since at most f replicas can be faulty.\n\t\t'
        if (len({a for (_, (_, _, a), (_ConstantPattern493_, _BoundPattern495_, _BoundPattern496_, _, _BoundPattern498_, _BoundPattern499_)) in self._ClientReceivedEvent_1 if (_ConstantPattern493_ == 'REPLY') if (_BoundPattern495_ == v) if (_BoundPattern496_ == self._state.clockValue) if (_BoundPattern498_ == self._state.cid) if (_BoundPattern499_ == r)}) >= (f + 1)):
            if (not (self._state.cid in self._state.results)):
                self._state.results[self._state.cid] = r
                prev_view = self._state.current_view
                self._state.current_view = v
                new_view = self._state.current_view
                self.send_liveness_result(prev_view, new_view)
                key = (self._state.current_view % len(self._state.replicas))
                self._state.primaryreplica = self._state.replicas[key]
    _Client_handler_431._labels = None
    _Client_handler_431._notlabels = None
