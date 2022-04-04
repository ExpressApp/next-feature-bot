`/help [command]`

Show short help for all commands or detailed help for specified command.

• `command_name` - Target command.

Examples:

```bash
# Show this help message
/help

# Show help for `/echo` command
/help /echo
```

**Available commands:**

% for command, description in sorted(bot_status.items()):
`${command}` -- ${description}
% endfor
