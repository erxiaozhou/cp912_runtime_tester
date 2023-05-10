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


payload确实是sign 段上的23位数

根据IEEE 754标准，每个NaN都应该属于canonical NaN或arithmetic NaN中的一个

在这段话中，subnormal是浮点数表示法中的一种特殊情况，也称为denormalized number。在IEEE 754标准中，每个浮点数都由一个符号位、指数和有效数字组成。对于正常的浮点数，最高位的有效数字一定是1，指数可以表示为2的幂次方。然而，对于subnormal数，最高位的有效数字是0，指数小于正常数最小的指数，从而允许更小的非规格化数值范围。Subnormal数可以表示非常接近于0的小数，但其精度通常较低。

NaN不属于subnormal也不属于normal，它是一种特殊的值。在IEEE浮点数标准中，NaN代表“不是一个数字”，通常用于指示一个无效的操作或结果。

Magnitude是一个浮点数表示中用来描述数值的部分，包括significand和exponent。在IEEE浮点数标准中，magnitude可以被表示为normal number或subnormal number的形式。Payload是指在某些特殊情况下，比如NaN值中，用来表示额外信息的位。在IEEE 754标准中，NaN值包含了一个payload，其中包含了关于NaN值的一些信息，如mantissa bits。

在IEEE 754标准中，NaN可以分为两种类型：quiet NaN和signaling NaN。quiet NaN是指在运算过程中出现了不合法的运算结果，而signaling NaN是指在运算中出现了一些被标记的条件，如除以零、对负数求平方根等，这些条件被称为“陷阱”（trap）。当运算结果为signaling NaN时，系统将抛出一个“陷阱”异常。


不是所有NaN都可以分类为canonical NaN或arithmetic NaN。实际上，IEEE 754标准定义了四种不同的NaN，其中两种是canonical NaN和arithmetic NaN，另外两种是quiet NaN和signaling NaN。canonical NaN和arithmetic NaN是指由操作（例如除以零或无穷大减去无穷大）产生的特定类型的NaN，而quiet NaN和signaling NaN是指由用户生成的NaN，通常用于表示无效操作或错误条件。

subnormal数和NaN是两个不同的概念，在float中不会存在subnormal的NaN。

如果指数= 并且尾数的小数部分非0，这个数表示为不是一个数（NaN）。（百度百科）
可以确定subnormal和NaN是两回事


0开头作为payload的NaN到底算什么

目前认为0开头的NaN不该存在


• All operators use “non-stop” mode, and floating-point exceptions are not otherwise observable. In particular, neither alternate floating-point exception handling attributes nor operators on status flags are supported. There is no observable difference between quiet and signalling NaN

Some operators are non-deterministic, because they can return one of several possible results (such as different NaN values). Technically, each operator thus returns a set of allowed values. For convenience, deterministic results are expressed as plain values, which are assumed to be identified with a respective singleton set.


Some operators are partial, because they are not defined on certain inputs. Technically, an empty set of results is returned for these inputs

没有见到nan只分为anan和cnan的表述

When the result of a floating-point operator other than fneg, fabs, or fcopysign is a NaN, then its sign is nondeterministic and the payload is computed as follows




