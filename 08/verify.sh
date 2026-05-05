#!/bin/bash

# Stop execution on any error
set -e

# Path to CPUEmulator relative to the 08 directory
EMULATOR=../tools/CPUEmulator.sh

echo "==============================================="
echo "    Starting Project 8 Verification"
echo "==============================================="
echo ""

# ---------------------------------------------
# 1. BasicLoop
# ---------------------------------------------
echo "[1/6] Processing: BasicLoop"
echo "   -> Running VMTranslator to translate .vm to .asm..."
python3 VMTranslator/VMTranslator.py ProgramFlow/BasicLoop/BasicLoop.vm

echo "   -> Running CPUEmulator for verification..."
$EMULATOR ProgramFlow/BasicLoop/BasicLoop.tst
echo "BasicLoop verification passed!"
echo "-----------------------------------------------"

# ---------------------------------------------
# 2. FibonacciSeries
# ---------------------------------------------
echo "[2/6] Processing: FibonacciSeries"
echo "   -> Running VMTranslator to translate .vm to .asm..."
python3 VMTranslator/VMTranslator.py ProgramFlow/FibonacciSeries/FibonacciSeries.vm

echo "   -> Running CPUEmulator for verification..."
$EMULATOR ProgramFlow/FibonacciSeries/FibonacciSeries.tst
echo "FibonacciSeries verification passed!"
echo "-----------------------------------------------"

# ---------------------------------------------
# 3. SimpleFunction
# ---------------------------------------------
echo "[3/6] Processing: SimpleFunction"
echo "   -> Running VMTranslator to translate .vm to .asm..."
python3 VMTranslator/VMTranslator.py FunctionCalls/SimpleFunction/SimpleFunction.vm

echo "   -> Running CPUEmulator for verification..."
$EMULATOR FunctionCalls/SimpleFunction/SimpleFunction.tst
echo "SimpleFunction verification passed!"
echo "-----------------------------------------------"

# ---------------------------------------------
# 4. NestedCall
# ---------------------------------------------
echo "[4/6] Processing: NestedCall"
echo "   -> Running VMTranslator to translate directory to .asm..."
python3 VMTranslator/VMTranslator.py FunctionCalls/NestedCall

echo "   -> Running CPUEmulator for verification..."
$EMULATOR FunctionCalls/NestedCall/NestedCall.tst
echo "NestedCall verification passed!"
echo "-----------------------------------------------"

# ---------------------------------------------
# 5. FibonacciElement
# ---------------------------------------------
echo "[5/6] Processing: FibonacciElement"
echo "   -> Running VMTranslator to translate directory to .asm..."
python3 VMTranslator/VMTranslator.py FunctionCalls/FibonacciElement

echo "   -> Running CPUEmulator for verification..."
$EMULATOR FunctionCalls/FibonacciElement/FibonacciElement.tst
echo "FibonacciElement verification passed!"
echo "-----------------------------------------------"

# ---------------------------------------------
# 6. StaticsTest
# ---------------------------------------------
echo "[6/6] Processing: StaticsTest"
echo "   -> Running VMTranslator to translate directory to .asm..."
python3 VMTranslator/VMTranslator.py FunctionCalls/StaticsTest

echo "   -> Running CPUEmulator for verification..."
$EMULATOR FunctionCalls/StaticsTest/StaticsTest.tst
echo "StaticsTest verification passed!"
echo "==============================================="
echo "All Project 8 tests passed!"
echo "==============================================="
