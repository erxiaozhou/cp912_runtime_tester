A **canonical NaN** is a floating-point value ±nan(canon𝑁) where canon𝑁 is a payload whose most significant bit
is 1 while all others are 0
payload部分最高有效位为1，其余为0的nan是canonical nan,numpy里面的两个/四个nan应该就是这种
An **arithmetic NaN** is a floating-point value ±nan(𝑛) with 𝑛 ≥ canon𝑁, such that the most significant bit is 1
while all others are arbitrary.
要求最高位是1，其他任意

spec后面有关于nan{}的内容，

从下面的描述看
signif(32) = 23 expon(32) = 8
signif(64) = 52 expon(64) = 11
canon𝑁 = 2^{signif(𝑁)−1}

