(module
  (type (;0;) (func))
  (type (;1;) (func (result i32)))
  (type (;2;) (func (result f32)))
  (func (;0;) (type 0)
    i32.const 1
    drop)
  (func (;1;) (type 1) (result i32)
    (local i32)
    i32.const 15)
  (func (;2;) (type 2) (result f32)
    (local i32 i32 i64 i64 f32 f32 f64 f64)
    i32.const 305419896
    local.set 0
    i32.const 1343229711
    local.set 1
    i64.const -72057589709208571
    local.set 2
    i64.const 1311768467463790335
    local.set 3
    f32.const 0x1.8cp+6 (;=99;)
    local.set 4
    f32.const 0x1.4d6466p+73 (;=1.23e+22;)
    local.set 5
    f64.const 0x1.5f0b08c960a79p+109 (;=8.9e+32;)
    local.set 6
    f64.const 0x1.570a3d70a3d71p+0 (;=1.34;)
    local.set 7
    f32.const -nan:0x333804 (;=-nan;)
    f32.abs)
  (func (;3;) (type 1) (result i32)
    i32.const 15)
  (table (;0;) 3 3 funcref)
  (memory (;0;) 1)
  (global (;0;) (mut i32) (i32.const 53167))
  (global (;1;) (mut i64) (i64.const -3476867894584379248))
  (export "memory" (memory 0))
  (export "_start" (func 2))
  (elem (;0;) (i32.const 0) func 1 0 3)
  (data (;0;) (i32.const 0) "Thiis is memory")
  (data (;1;) (i32.const 16) "\5c12\5c34\5c56\5c78\5c9a\5cbc\5cde\5cff"))
