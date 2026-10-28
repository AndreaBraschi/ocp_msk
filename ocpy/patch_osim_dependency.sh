#!/bin/bash
# This script was written with the support of Qwen3.7-Plus.
# This script intends to solve the issue described here: https://github.com/opensim-org/opensim-core/issues/4312.
# Long story short, in a Linux distro (Ubuntu 22.04), there is conflict when uv pip installing CasADi as a standalone package alongside OpenSim.
# Moco, along with its own specific version of CasADi (i.e. 3.6.5), are built into the OpenSim wheel. Therefore, when uv pip install opensim, they all come from the same installation.
# This may create conflict when importing either one of them, if the standalone version of CasADi differs from the Moco's one.
# Specifically, both compiled versions of CasADi (standalone and Moco) share the same file name: libcasadi.so.3.7 (compiled casadi for Linux). 
# This name is referenced in the dynamic links, which are built when the projects get compiled. 
# In Python, when importing CasADi first, for example, the loader grabs the .so file name and uses this to load the specific CasADi version that came with CasADi installation. 
# Then, OpenSim is imported (import opensim), which is linked to libosimMoco.so and this is linked to libcasadi.so.3.7. This should reference Moco's own version of CasADi (3.6.5), but
# file name libcasadi.so.3.7 (as a plain string) was already registered from the previous import, and the loader simply skips it, therefore, not loading Moco's own version of CasADi and keeping 
# that was previously imported (3.8.1) and is already in memory, which fails the import as this version isn't compatible with the version that is required by Moco (it simply breaks as the 2 versions 
# may have different APIs, features, etc.). The import would equally fail were the order be inverted, for the same incompatibilities between the 2 versions. However, it may also be that the 2 versions,
# although different, match up well and no error is thrown.


package_name="opensim"
old_lib_name="libcasadi.so.3.7"
new_lib_name="osim_libcasadi.so.3.7"

# find the path to the dir of the problematic package
pkg_dir=$(python -c "import $package_name, os; print(os.path.dirname($package_name.__file__))")

# path to target lib
target_lib=$(find "$pkg_dir" -name "$old_lib_name" | head -n 1)

[ -z "$target_lib" ] && exit 0

# new full path to renamed lib
new_path="$(dirname "$target_lib")/$new_lib_name"

# change location
mv "$target_lib" "$new_path"

# rename .so file
patchelf --set-soname "$new_lib_name" "$new_path"

for ext in $(find "$pkg_dir" -name "*.so"); do
    [ "$ext" = "$new_path" ] && continue
    if patchelf --print-needed "$ext" 2>/dev/null | grep -qx "$old_lib_name"; then
        patchelf --replace-needed "$old_lib_name" "$new_lib_name" "$ext"
    fi
done