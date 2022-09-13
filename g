printf "============================================\n"
set $ipx = 0
while ($ipx < ProcGlobal->allProcCount)
   if (ProcGlobal->allPgXact[$ipx]->overflowed)
        printf "pid index: %d\n", $ipx
        printf "pid of overflowed trx: %d\n", ProcGlobal->allProcs[$ipx]->pid
        printf "number of subtrx: %d\n", ProcGlobal->allPgXact[$ipx]->nxids
        printf "session id of the trx: %d\n", ProcGlobal->allProcs[$ipx]->mppSessionId
        printf "roleId of the pid: %d\n", ProcGlobal->allProcs[$ipx]->roleId
	printf "~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
   end
   set $ipx = $ipx + 1
end
printf "============================================\n"
quit
