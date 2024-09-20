console.log("tools")
const cut_title = (title) => {
    // cut the string to 19 characters and add ... if it's longer than 19 characters
    return title.length > 19 ? title.slice(0, 19) + "..." : title
}
const get_extension = (title) => {
    return title.split(".").pop()
}
export {cut_title,get_extension}