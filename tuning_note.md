randomByteMutationLimitbyLogTester 0704版调参记录

参数估算
目前估算，这个tester 生成的case的数量，应该是 log type 的数量 X mutate_num X max_log_appear_num
以 v18.1_subsetv2_raw_mutation2_2 为参考设计调参方案， 
该次执行里有 158,000 mutations , 
all_log_category 里面有 79 种 key
only_interesting_log_category 里面有 38 种 key
only_highlight_log_category 里面有 20 种 key

因为目前的 randomByteMutationLimitbyLogTester 以 all 为标准， 所以要覆盖所有的 all_log_category 里面的 key的话，若  mutate_num X max_log_appear_num > 2000，那么生成的 tcs 数量会超过 v18.1_subsetv2_raw_mutation2_2 中生成的数量
也就是 2000 是 两个参数乘积的上限，而不是下限。在能cover 到足够多（这里就是79种） log type 就好


main_testing_v18_330_9811_2
1,279,491 次mutate, 
all_log_category ： 298 
only_interesting_log_category : 120
only_highlight_log_category : 63

这时的上限是 4000+ ， 



要注意的：
看看能不能加个优先级的设置，比如 比较少见的 log type变出的东西，优先mutate
注意下存储 tc_paths 所占用的空间





5501 的小数据集上跑出的结果看， only_highlight上分别有 22 22 21 20 19 个key 
强行终止的 all 级别的 LimitLog 上跑出了 20个key 

only_interesting 级别的logLimit (参数：10，,10)上跑出了 28 / 25 / 10 个 only_highlight 级别的key,但是wrong alignment出的不稳定

268,230 次mutate 约1小时
28 25 10

only_interesting 级别的logLimit (参数：5，,10) 都是10左右的 only_highlight 级别的key


跑了一天
only_interesting 级别的logLimit (参数：20，,10) 64 的 only_highlight 级别的key ; ((wasm3_dump, (CanExecute,))上测出了 37 个组合
