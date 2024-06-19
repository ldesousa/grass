"""Test of r.out.gdal
@author Luís Moreira de Sousa
"""

from pathlib import Path
from grass.gunittest.case import TestCase


class TestOgrExport(TestCase):

    # Vector map in NC test dataset
    test_map = "boundary_county_500m"

    # Result of import tests
    temp_import = "test_gdal_import_map"

    # Output of r.univar
    univar_string = """n=616509
null_cells=506073
cells=1122582
min=0
max=199
range=199
mean=87.1764564669778
mean_of_abs=87.1764564669778
stddev=62.4325833627095
variance=3897.82746534167
coeff_var=71.6163352961689
sum=53745070
"""

    @classmethod
    def setUpClass(cls):
        """Use temporary region settings"""
        cls.use_temp_region()

    @classmethod
    def tearDownClass(cls):
        """!Remove the temporary region"""
        cls.del_temp_region()

    def tearDown(self):
        self.runModule(
            "g.remove", type="raster", flags="f", pattern=f"{self.temp_import}*"
        )
        for p in Path(".").glob(f"{self.test_map}*"):
            p.unlink()

    def test_gpkg_format(self):
        """Tests output to GeoPackage format"""

        self.runModule("g.region", raster=self.test_map)

        self.assertModule(
            "r.out.gdal",
            "Export to GeoPackage Format",
            input=self.test_map,
            output=f"{self.test_map}.gpkg",
            format="GPKG",
            type="Int16",
            flags="f",
        )

        # Import back to verify
        self.runModule(
            "r.in.gdal",
            input=f"{self.test_map}.gpkg",
            output=self.temp_import,
        )

        self.assertRasterFitsUnivar(
            raster=self.temp_import,
            reference=self.univar_string,
            precision=1e-8,
        )

    def test_gtiff_format(self):
        """Tests output to GeoTiff format"""

        self.runModule("g.region", raster=self.test_map)

        self.assertModule(
            "r.out.gdal",
            "Export to GeoTiff Format",
            input=self.test_map,
            output=f"{self.test_map}.gtiff",
            format="GTiff",
            type="Int16",
            flags="fc",
        )

        # Import back to verify
        self.runModule(
            "r.in.gdal",
            input=f"{self.test_map}.gtiff",
            output=self.temp_import,
        )

        self.assertRasterFitsUnivar(
            raster=self.temp_import,
            reference=self.univar_string,
            precision=1e-8,
        )


if __name__ == "__main__":
    from grass.gunittest.main import test

    test()
