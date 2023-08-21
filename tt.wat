(module
  (type (;0;) (func))
  (type (;1;) (func (result f64)))
  (func (;0;) (type 1) (result f64)
    f64.const -nan:0x8001a14000000 (;=-nan;)
    f64.const 0x1.000f600f00084p+17 (;=131103;)
    return
    select (result f64))
  (export "_start" (func 0))
  (export "to_test" (func 0)))
