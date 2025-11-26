module AddSubArea(
  input        clock,
  input        reset,
  input  [7:0] io_a,
  input  [7:0] io_b,
  input        io_sub,
  output [7:0] io_out
);
  wire [7:0] _b_eff_T_1 = 8'h0 - io_b;
  wire [7:0] b_eff = io_sub ? _b_eff_T_1 : io_b;
  assign io_out = io_a + b_eff;
endmodule
