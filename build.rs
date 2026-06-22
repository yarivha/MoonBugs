// build.rs — embeds the Windows .exe icon (and version metadata) into the
// binary when building for a Windows target. On every other target this is a
// no-op, so it doesn't affect macOS/Linux builds.
//
// `winresource` is a plain build-dependency (compiled for the host) so this
// file always type-checks; the actual resource compilation only runs for
// Windows targets. It needs a resource compiler (MSVC's rc.exe when building
// natively on Windows, or llvm-rc / mingw windres when cross-compiling). If
// none is found we warn and continue rather than failing the build.

fn main() {
    let target_os = std::env::var("CARGO_CFG_TARGET_OS").unwrap_or_default();
    if target_os == "windows" {
        let mut res = winresource::WindowsResource::new();
        res.set_icon("assets/icon.ico");
        res.set("ProductName", "Moon Bugs");
        res.set("FileDescription", "Moon Bugs — Lunar Defense");
        if let Err(e) = res.compile() {
            println!("cargo:warning=could not embed Windows icon: {e}");
        }
    }
    println!("cargo:rerun-if-changed=assets/icon.ico");
}
