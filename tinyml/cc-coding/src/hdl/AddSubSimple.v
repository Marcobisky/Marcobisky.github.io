module AddSubSimple(
  input        clock,
  input        reset,
  input  [7:0] io_a,
  input  [7:0] io_b,
  input        io_sub,
  output [7:0] io_out
);
  wire [7:0] addRes = io_a + io_b;
  wire [7:0] subRes = io_a - io_b;
  assign io_out = io_sub ? subRes : addRes;
endmodule
