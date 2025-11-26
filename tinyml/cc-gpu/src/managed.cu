#include <stdio.h>
#include <cuda_runtime.h>

__global__ void my_kernel(int* x_ptr) {
    *x_ptr = 1;
    printf("GPU sees x = %d\n", *x_ptr);
}

int main() {
    int x = 0;
    int* x_ptr = &x;
    cudaMallocManaged(&x_ptr, sizeof(int));

    my_kernel<<<1,1>>>(x_ptr);

    printf("CPU sees x = %d\n", x);

    cudaFree(x_ptr);
    return 0;
}
