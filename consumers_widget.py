# %%
import json
import ipyvuetify as v

CONSUMERS_FILE = "data/consumers.json"

# %%
with open(CONSUMERS_FILE, "r") as f:
    CONSUMERS = json.load(f)

# %%


class ConsumerTable(v.Container):
    def __init__(self):
        self.consumers = CONSUMERS
        self.consumer_name = v.TextField(label="name", v_model="")
        self.consumer_usage = v.TextField(label="usage", v_model="")
        self.add_btn = v.Btn(class_="mb-2", children=[v.Icon(children=["mdi-plus"])])
        self.add_btn.on_event("click", self.add_consumer)
        self.add_consumer_row = v.Row(
            children=[self.consumer_name, self.consumer_usage, self.add_btn]
        )
        self.consumer_item_group = v.ListItemGroup(children=self.get_consumer_items())
        self.consumer_list = v.List(children=[self.consumer_item_group])
        super().__init__(
            children=[
                self.add_consumer_row,
                self.consumer_list,
            ]
        )

    def add_consumer(self, *args):
        self.consumers.append(
            {"name": self.consumer_name.v_model, "usage": self.consumer_usage.v_model}
        )

        with open(CONSUMERS_FILE, "w") as f:
            json.dump(self.consumers, f, indent=4)
        self.consumer_name.v_model = ""
        self.consumer_usage.v_model = ""
        self.refresh()

    def refresh(self):
        self.consumer_item_group.children = self.get_consumer_items()

    def get_consumer_items(self):
        def delete(button, *args):
            consumer = button.consumer_item
            self.consumers.remove(consumer)
            with open(CONSUMERS_FILE, "w") as f:
                json.dump(self.consumers, f, indent=4)
            self.refresh()

        consumer_items = []
        for consumer in self.consumers:
            delete_btn = v.Btn(children=[v.Icon(children=["mdi-delete-outline"])])
            delete_btn.consumer_item = consumer
            delete_btn.on_event("click", delete)

            consumer_items.append(
                v.ListItem(
                    children=[
                        v.ListItemContent(
                            children=[
                                consumer["name"],
                                v.Divider(class_="mx-4", vertical=True),
                                str(consumer["usage"]),
                            ]
                        ),
                        v.ListItemAction(children=[delete_btn]),
                    ]
                )
            )
        return consumer_items


# ConsumerTable()


# %%
