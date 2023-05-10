iwasm  : f64.max f32.copysign
    <!-- iwasm_nan1 -->
    f64.const nan:0x39 (;=nan;)
    f64.const -nan:0x2f000000 (;=-nan;)
    f64.max
    <!-- cp907_b3 -->
    f32.const -nan:0xefef4 (;=-nan;)
    f32.const -0x1.44ceeep+127 (;=-2.15872e+38;)
    f32.copysign


wasmi  : f64.max
    <!-- iwasm_nan1 /wasmi_nan -->
    f64.const nan:0x39 (;=nan;)
    f64.const -nan:0x2f000000 (;=-nan;)
    f64.max

wamsm3
    f32.const -0x1.b6ff18p+126 (;=-1.45882e+38;)
    f32.const -nan (;=-nan;)
    f32.max