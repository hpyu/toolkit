export ANDROID_SRC=/home/hpyu/src/aloe
export SYMBOL=/home/hpyu/issues/aloe/10_hang/dump/symbols
echo "set solib-absolute-prefix $SYMBOL" > cmds.gdb
echo "set solib-search-path $SYMBOL/system/lib/" >> cmds.gdb
echo "source /home/hpyu/toolkit/logcat.gdb" >> cmds.gdb
echo "logcat" >> cmds.gdb
time $ANDROID_SRC/prebuilts/gcc/linux-x86/arm/arm-eabi-4.8/bin/arm-eabi-gdb $SYMBOL/system/bin/logd $1 -batch -x cmds.gdb

