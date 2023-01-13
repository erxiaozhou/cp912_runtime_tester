ref.null的tc应该只有两条
ref.null func ; ref.null extern

ref.func有一个立即数参数
ref.func x

ref.is_null
有的地方（execution段看，后面有一个type立即数），但是自己试着加又加不上去
最后应该有4个tc
null funcref
null externref
non null funcref
non null externref
最后一个比较不好搞，可能要从table里面dump
