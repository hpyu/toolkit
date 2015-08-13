# Extract logcat log from logd coredump
# 
# Why make this tool:
#	Sometimes we need get logcat log from ramdump to check panic/hang issue.
#	Before Android5.0, Andorid log buffers are in kernel space, crash extension logcat can do it
#	Android5.0 move Android log buffers to userspace and managed by logd, so need extrace it from
#	logd coredump
#
#	Usage:
#		1. open ramdump by crash tool, get logd TGID
#			crash> ps -G | grep logd 
#		2. get coredump of logd
#			crash>gcore -v0 TGID  #replace TGID with real number
#		3. run script:
#			./gdb.sh gcore.TGID.logd  #replace TGID with real number
#		4. wait several minitues, Android log stored to logcat_logd.txt
#
#	Notice:
#		Change ANDROID_SRC, SYMBOL abd logcat.gdb path in your environment before run gdb.sh
#
#	content of gdb.sh:
#		cat gdb.sh
#		export ANDROID_SRC=/home/hpyu/src/aloe
#		export SYMBOL=/home/hpyu/issues/aloe/10_hang/dump/symbols
#		echo "set solib-absolute-prefix $SYMBOL" > cmds.gdb
#		echo "set solib-search-path $SYMBOL/system/lib/" >> cmds.gdb
#		echo "source /home/hpyu/toolkit/logcat.gdb" >> cmds.gdb
#		echo "logcat" >> cmds.gdb
#		time $ANDROID_SRC/prebuilts/gcc/linux-x86/arm/arm-eabi-4.8/bin/arm-eabi-gdb $SYMBOL/system/bin/logd $1 -batch -x cmds.gdb
#
#	Writen by Haipeng.Yu, hpyu@live.cn


define logcat_print_logbuf
	set $head = $arg0
	set $next = $head->mpNext
		
	while $next != $head

		if $next->mVal->mLogId == 2 || $next->mVal->mLogId == 5
			set $next = $next->mpNext
			loop_continue
		end

		set $entry = $next->mVal
		set $p = $entry->mMsg
		set $p1 = $p
		while *(char *)$p1 != 0
			set $p1 = $p1 + 1
		end
		set $p2  = $p1 + 1

		printf "%d.%d  LOGID:%d %d/%s (%d|%d) %s\n", $entry->mMonotonicTime.tv_sec, $entry->mMonotonicTime.tv_nsec, $entry->mLogId, *(char *)$p, $p+1, $entry->mPid, $entry->mTid, $p2

		set $next = $next->mpNext

	end
end

define logcat
	dont-repeat

	thread 2
	frame 2
	set pagination off
	set logging file logcat_logd.txt
	set logging on

	printf "Extract Android log, LOG_ID as below, omit RADIO and KERNEL log, store to logcat_logd.txt\n"
	printf "LOG_ID_MAIN   = 0\n"
	printf "LOG_ID_RADIO  = 1\n"
	printf "LOG_ID_EVENTS = 2\n"
	printf "LOG_ID_SYSTEM = 3\n"
	printf "LOG_ID_CRASH  = 4\n"
	printf "LOG_ID_KERNEL = 5\n"

	logcat_print_logbuf this->mLogbuf->mLogElements->mpMiddle

	set logging off
	set pagination on
end

document logcat
	Extract Android log from logd and save to logcat_logd.txt.
	Syntax: logcat
	Note: the extracted log are mixed with below log buffer.
	Buffer id:
		LOG_ID_MAIN = 0,     
		LOG_ID_RADIO = 1,    
		LOG_ID_EVENTS = 2,   
		LOG_ID_SYSTEM = 3,   
		LOG_ID_CRASH = 4,    
		LOG_ID_KERNEL = 5,

end

