define plogbuf_list
	set $id = $arg0
	set $head = $arg1
	set $next = $head->mpNext
	
	if $id == 0
		printf "============== MAIN log ==============\n"
	end
	if $id == 1
		printf "============== RADIO log ==============\n"
	end
	if $id == 2
		printf "============== EVENTS log ==============\n"
	end
	if $id == 3
		printf "============== SYSTEM log ==============\n"
	end
	if $id == 4
		printf "============== CRASH log ==============\n"
	end
	if $id == 5
		printf "============== KERNEL log ==============\n"
	end
	
	while $next != $head

		if $next->mVal->mLogId != $id
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

		printf "%d.%d  %d/%s (%d|%d) %s\n", $entry->mMonotonicTime.tv_sec, $entry->mMonotonicTime.tv_nsec, *(char *)$p, $p+1, $entry->mPid, $entry->mTid, $p2

		set $next = $next->mpNext

	end
end

# LOG_ID_MAIN = 0,     
# LOG_ID_RADIO = 1,    
# LOG_ID_EVENTS = 2,   
# LOG_ID_SYSTEM = 3,   
# LOG_ID_CRASH = 4,    
# LOG_ID_KERNEL = 5,

define logcat
	dont-repeat
	# change your symbol path accordingly
	#set solib-search-path /home/hpyu/src/aloe/out/target/product/pxa1936aloe/symbols/system/lib/
	#set solib-absolute-prefix  /home/hpyu/src/aloe/out/target/product/pxa1936aloe/symbols/
	set solib-search-path /home/hpyu/issues/aloe/10_hang/dump/symbols/system/lib/
	set solib-absolute-prefix  /home/hpyu/issues/aloe/10_hang/dump/symbols/
	
	#thread apply 2 bt
	thread 2
	frame 2
	set pagination off
	set logging file logcat_from_logd.txt
	set logging on

	set $id = 0
	if $argc == 0
		help logcat
		set $num = 1
	else
		set $num = $arg0
		if $num > 6
			set $num = 6
		end
	end

	printf "id = %d, num = %d\n", $id, $num
	
	while $id < $num
		plogbuf_list $id (this->mLogbuf->mLogElements->mpMiddle)

		set $id = $id + 1
	end

	set logging off
	set pagination on
end

document logcat
	Extract Android log from logd and save to logcat_from_logd.txt.
	Syntax: pvector <num>
	Note: <num> is the number of buffer to extract, from 1 to 6 are main|audio|events|system|crash|kernel
	Buffer id:
		LOG_ID_MAIN = 0,     
		LOG_ID_RADIO = 1,    
		LOG_ID_EVENTS = 2,   
		LOG_ID_SYSTEM = 3,   
		LOG_ID_CRASH = 4,    
		LOG_ID_KERNEL = 5,

	Examples:
	logcat - get main log by default
	logcat 2 - get main and audio log buffer
	logcat 5 - get all log buffer
end

