# eazyscript
Easy peasy application building

Tags

Visual Tags
- application
- layout
- component

Data Tags
- state
- event
- query


## Introduction

This is a very easy scripting language that lets you build applications extremely fast with very little code. It is a very high level language that abstracts away a lot of the complexity of building applications. It is designed to be very easy to learn and use, and to be very flexible and powerful.

## Getting Started

To get started, you need to install the eazyscript compiler. You can do this by running the following command:

```
npm install -g eazyscript
```

Once you have installed the compiler, you can start writing eazyscript code. Here is an example of a simple eazyscript program that creates a window with a button:

```
application type:web
  layout type:window
    component type:button
      text: "Click me"
      onClick:
        alert("Button clicked!")
```

To compile this code, save it to a file called `example.ez` and run the following command:

```
eazyscript example.ez
```

This will compile the code and generate a JavaScript file called `example.js` that you can run in your browser.

## Documentation

For more information on how to use eazyscript, check out the [documentation](https://eazyscript.com/docs).

## Examples

Here are some examples of eazyscript code:

### Hello World

```
application type:web
  layout type:window
    component type:text
      text: "Hello, world!"

```

### Counter

```
application type:web
  layout type:window
    layout type:column
      var: count
      component type:text
        text: $count
        css:
          fontSize: 24
          fontWeight: bold
          margin: 10
      component type:button
        text: "Increment"
        onClick: $count++
        height: 50
        width: 100
```

### Todo List

```
application type:web
  layout type:window
    layout type:column
      var: todos
      var: todo
      component type:input
        var: $todo
        placeholder: "Enter todo"
        width: 200
        margin: 10
      component type:button
        text: "Add"
        onClick: $todos.append($todo)
      component type:list
        items: $todos
```

## Contributing

If you would like to contribute to eazyscript, please check out the [contribution guidelines](https://eazyscript.com/contribute).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```


