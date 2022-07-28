## Block concept
- To do multiple tasks with same `when` condition or similar

```
- name: Main Task
  block:
    - name: Get subtask1
      set_fact:
        task1: "subtask1"
    - name: Get subtask2
      set_fact:
        task2: "subtask2"       
    - name: Get subtask3
      include_tasks: "my-common-task.yaml"
      loop: "{{my_list | list }}"
      loop_control:
        loop_var: fruit
  when: env_input is defined
 ```
