This is a [Maubot](https://github.com/maubot/maubot) plugin for use in a [Matrix](https://matrix.org/) chat room. The plugin allows you to define arbitrary emoji reactions that will cause messages tagged with the specified emoji to be automatically cross-posted to a different room.

Example use cases could be tagging messages with :bulb: to post them to an #ideas channel for follow-up. Or if a message is off-topic, an emoji-reaction (say :train:) could cause the message to be reposted to the room with the correct topic for further discussion (say #public_transportation).

You'll need to create a config.yaml (based on [example-config.yaml](example-config.yaml)) to specify mappings. For example:
```
mapping:
  💡: 'ideas'
  🚋: 'public_transportation'
```
Will cause any message tagged with the bulb emoji :bulb: to be posted to the local room with the alias #ideas and the train emoji :train: to be posted to the local room with the alias #public_transportation. You can define as many actions as you want, although currently the plugin is limited to posting to one room per emoji reaction.

In the cross-posted channel, the message will have the emoji that caused the cross-post appended to the end which serves as a hyperlink back to the original message, as well as the name of the user who caused the cross-post.

Note the YAML parser is fussy and needs a space after the colon for the mapping to work correctly. You will also need to put the room name in quotes if you use the fully qualified room name (!room_id:server.tld) as opposed to the alias.

## Important security warning
If `insecure` is set to `true` (the default setting), the plugin will post from any room defined in the configuration to any other room defined in the configuration, regardless of encryption of the source and destination rooms. So, depending on how you configure it, you could have it post from an encrypted room to a non-encrypted room (or vice-versa), so long as your maubot client is in both rooms. If you want to prohibit this behavior, set `insecure` in config.yaml to `false`.

## TODO 

* add in-room commands to define mappings
* cull back unnecessary libraries
* allow multiple room posting with single emoji
