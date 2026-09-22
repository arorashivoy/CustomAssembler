var total
mov R1 $0
mov R2 $1
mov R3 $10
loop: add R1 R2 R1
cmp R1 R3
jlt loop
st R1 total
hlt
