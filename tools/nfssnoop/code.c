#include <linux/sched.h>
#include <linux/sunrpc/sched.h>

// define output data structure in C
struct data_t {
  u32 pid;
  u64 ts;
  char comm[TASK_COMM_LEN];
  u32 statidx;
  // char path[PATH_MAX];
};

BPF_PERF_OUTPUT(events);

struct rpc_procinfo {
  u32 p_proc;            /* RPC procedure number */
  kxdreproc_t p_encode;  /* XDR encode function */
  kxdrdproc_t p_decode;  /* XDR decode function */
  unsigned int p_arglen; /* argument hdr length (u32) */
  unsigned int p_replen; /* reply hdr length (u32) */
  unsigned int p_timer;  /* Which RTT timer to use */
  u32 p_statidx;         /* Which procedure to account */
  const char *p_name;    /* name of procedure */
};

int hello(struct pt_regs *ctx, struct rpc_task_setup *task_setup_data) {
  struct data_t data = {};
  data.pid = bpf_get_current_pid_tgid();
  data.ts = bpf_ktime_get_ns();
  bpf_get_current_comm(&data.comm, sizeof(data.comm));
  data.statidx = task_setup_data->rpc_message->rpc_proc->p_statidx;
  events.perf_submit(ctx, &data, sizeof(data));
  return 0;
}
