#include <stdio.h>

#define NR_CPUS 4
#define FTRACE_LOG_MAX 8192
#define MAX_TEXT_LEN    135

struct event_log {
	unsigned long long time;
	char cpu;
	char text[MAX_TEXT_LEN];
};

struct ftrace_log {
	struct event_log event[NR_CPUS][FTRACE_LOG_MAX];
};

struct ftrace_log trace_buf;

FILE *open_event_log(cpu)
{
	char name[32];
	FILE *fp = NULL;
	snprintf(name, sizeof(name), "e%d.log", cpu);
	fp = fopen(name, "w");
	if (fp == NULL) {
		printf("%s creat failed!!", name);
	}

	return fp;
}

int main(int argc, char *argv[])
{
	struct ftrace_log trace_buf;
	FILE *fp_bin = NULL;
	FILE *fp_log = NULL;
	int cpu, i,j, ret;
	struct event_log *p = NULL;
	unsigned long long lasttime;
	int start_pos[NR_CPUS] = {0, 0, 0, 0};

	if (argc < 2) {
		printf("Usage: %s ftrace.bin\n", argv[0]);
		return -1;
	}

	fp_bin = fopen(argv[1], "rb");
	if (fp_bin == NULL) {
		printf("Failed to open %s\n", argv[1]);
		return -1;
	}

	ret = fread(&trace_buf, sizeof(struct ftrace_log), 1, fp_bin);	
	for (cpu = 0; cpu < NR_CPUS; cpu++){
		if ((fp_log = open_event_log(cpu)) == NULL)
			return -1;

		fprintf(fp_log, "==================== cpu %d ========================\n", cpu);
		lasttime = trace_buf.event[cpu][0].time;
		for (i = 1; i < FTRACE_LOG_MAX; i ++){
			p = &trace_buf.event[cpu][i];
			if (p->time < lasttime)	{
				start_pos[cpu] = i;
				break;
			} else {
				lasttime = p->time;
			}
		}

		for (i = 0; i < FTRACE_LOG_MAX; i ++){
			p = &trace_buf.event[cpu][(i+start_pos[cpu]) % FTRACE_LOG_MAX];
			p->text[MAX_TEXT_LEN-1] = '\0';
			fprintf(fp_log, "%d %8.9f %s\n\n", p->cpu, (double)p->time/1000000000, p->text);
		}

		fclose(fp_log);
	}

	fclose(fp_bin);

	return 0;
}


