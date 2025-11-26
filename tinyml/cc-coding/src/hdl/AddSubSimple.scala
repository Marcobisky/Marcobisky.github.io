class AddSubSimple extends Module {
  val io = IO(new Bundle {
    val a = Input(UInt(8.W))
    val b = Input(UInt(8.W))
    val sub = Input(Bool())   // true 表示减法
    val out = Output(UInt(8.W))
  })

  // 两个独立运算单元
  val addRes = io.a + io.b
  val subRes = io.a - io.b

  io.out := Mux(io.sub, subRes, addRes)
}