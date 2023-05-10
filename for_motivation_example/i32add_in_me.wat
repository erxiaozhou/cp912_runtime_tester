(module
  (type (;0;) (func))
  (type (;1;) (func (result i32)))
  (func (;0;) (type 1) (result i32)
    (local i32 f32 i64 f64)
    i32.const 5
    i32.const 10
    i32.add)
  (export "_start" (func 0))
  (export "to_test" (func 0)))
