class AddSubOptimized extends Module {
  val io = IO(new Bundle {
    val a = Input(UInt(8.W))
    val b = Input(UInt(8.W))
    val sub = Input(Bool())
    val out = Output(UInt(8.W))
  })

  // 如果是减法，就取 -B；否则取 B
  val b_eff = Mux(io.sub, -io.b, io.b)
  io.out := io.a + b_eff
}