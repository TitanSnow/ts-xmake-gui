add_subdirs(path.join("winpty","src"))
target("capture_output")
    set_kind("shared")
    add_includedirs("$(buildir)")
    add_linkdirs("$(buildir)")
    add_links("winpty")
    add_deps("winpty")
    add_files("capture_output.c")
    set_warnings("all")
