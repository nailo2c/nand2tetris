#!/bin/bash

# Stop execution on any error
set -e

# Path to CPUEmulator relative to the 07 directory
EMULATOR=../tools/CPUEmulator.sh

echo "==============================================="
echo "    Starting Verification Script"
echo "==============================================="
echo ""

# ---------------------------------------------
# 1. BasicTest
# ---------------------------------------------
echo "⏳ [1/5] Processing: BasicTest"
echo "   -> Running VMTranslator to translate .vm to .asm..."
python3 VMTranslator/VMTranslator.py MemoryAccess/BasicTest/BasicTest.vm

echo "   -> Running CPUEmulator for verification..."
$EMULATOR MemoryAccess/BasicTest/BasicTest.tst
echo "✅ BasicTest verification passed!"
echo "-----------------------------------------------"

# ---------------------------------------------
# 2. PointerTest
# ---------------------------------------------
echo "⏳ [2/5] Processing: PointerTest"
echo "   -> Running VMTranslator to translate .vm to .asm..."
python3 VMTranslator/VMTranslator.py MemoryAccess/PointerTest/PointerTest.vm

echo "   -> Running CPUEmulator for verification..."
$EMULATOR MemoryAccess/PointerTest/PointerTest.tst
echo "✅ PointerTest verification passed!"
echo "-----------------------------------------------"

# ---------------------------------------------
# 3. StaticTest
# ---------------------------------------------
echo "⏳ [3/5] Processing: StaticTest"
echo "   -> Running VMTranslator to translate .vm to .asm..."
python3 VMTranslator/VMTranslator.py MemoryAccess/StaticTest/StaticTest.vm

echo "   -> Running CPUEmulator for verification..."
$EMULATOR MemoryAccess/StaticTest/StaticTest.tst
echo "✅ StaticTest verification passed!"
echo "-----------------------------------------------"

# ---------------------------------------------
# 4. SimpleAdd
# ---------------------------------------------
echo "⏳ [4/5] Processing: SimpleAdd"
echo "   -> Running VMTranslator to translate .vm to .asm..."
python3 VMTranslator/VMTranslator.py StackArithmetic/SimpleAdd/SimpleAdd.vm

echo "   -> Running CPUEmulator for verification..."
$EMULATOR StackArithmetic/SimpleAdd/SimpleAdd.tst
echo "✅ SimpleAdd verification passed!"
echo "-----------------------------------------------"

# ---------------------------------------------
# 5. StackTest
# ---------------------------------------------
echo "⏳ [5/5] Processing: StackTest"
echo "   -> Running VMTranslator to translate .vm to .asm..."
python3 VMTranslator/VMTranslator.py StackArithmetic/StackTest/StackTest.vm

echo "   -> Running CPUEmulator for verification..."
$EMULATOR StackArithmetic/StackTest/StackTest.tst
echo "✅ StackTest verification passed!"
echo "==============================================="
echo " 🎉 Congratulations! All tests passed!"
echo "==============================================="
