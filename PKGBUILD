# Maintainer: NoahC500
pkgname=habbo-mi-helper
pkgver=0.1.5
pkgrel=1
pkgdesc="This is a script I've created to aid me in my role as Director General of Military Intelligence at HabboUK."
arch=('any')
url="https://github.com/NoahC500/habbo-mi-helper"
license=('GPL')
depends=(
	'python'
	'python-requests'
	'tk'
	'python-pillow'
)
source=(
	"Script.py"
	"Logo.png"
	"README.md"
	"habbo-mi-helper.desktop"
)
sha256sums=(
	"c8333669f84e99ccea7eec28ecd708ff2ccd4570f3f5518a7ca5a7d4f85552c4"
	"75942aa97d6a0318e8a103dcb6a051be277c70213fdd12c5a01611e36668d61c"
	"f3a9fa2bcc46ee97138ab0cf89e0309e4710797538842e906a667875e490104f"
	"d9e8c724bb42f09d6c108ced0695fecc755b2cee5cf9b02c2bd00fb520502097"
)

package() {
	cd "$srcdir"
	mkdir "$pkgdir/usr/bin/habbo-mi-helper/" -p
	install -m 0755 "./Script.py" "$pkgdir/usr/bin/habbo-mi-helper/habbo-mi-helper.py"
	install -m 0744 "./Logo.png" "$pkgdir/usr/bin/habbo-mi-helper/icon.png"
	install -m 0744 "./README.md" "$pkgdir/usr/bin/habbo-mi-helper/"

	mkdir "$pkgdir/usr/share/applications/" -p
	install -m 0755 "./habbo-mi-helper.desktop" "$pkgdir/usr/share/applications/"
}
