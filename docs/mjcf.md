# MJCF Generation

Install the converter:

```bash
pip install "urdf-to-mjcf>=0.1.1"
```

The converter is maintained at <https://github.com/discoverse-dev/urdf-to-mjcf>.
Run the following commands from the package root.

## Wheeled Base

`mjcf/galbot_one_golf.xml` is the main MuJoCo model. It uses the full URDF,
keeps the four wheel joints, and adds wheel velocity actuators.

```bash
urdf-to-mjcf urdf/galbot_one_golf.urdf \
  --output mjcf/galbot_one_golf.xml \
  --metadata config/mjcf/metadata_wheeled.json \
  --default-metadata config/mjcf/default.json config/mjcf/default_wheeled.json \
  --actuator-metadata config/mjcf/actuator.json config/mjcf/actuator_wheeled.json \
  --appendix config/mjcf/appendix.xml \
  --collision-type mesh
```

## Fixed Base

`mjcf/galbot_one_golf_fixed_base.xml` has no mobile-base or wheel-drive joints.
Use it for fixed-base checks, manipulation-only workflows, and static model
inspection.

```bash
urdf-to-mjcf urdf/galbot_one_golf_fixed_base.urdf \
  --output mjcf/galbot_one_golf_fixed_base.xml \
  --metadata config/mjcf/metadata.json \
  --default-metadata config/mjcf/default.json \
  --actuator-metadata config/mjcf/actuator.json \
  --appendix config/mjcf/appendix.xml \
  --collision-type mesh
```

## Planar Base

`mjcf/galbot_one_golf_planar_base.xml` uses virtual planar base joints:
`base_x_joint`, `base_y_joint`, and `base_yaw_joint`.

```bash
urdf-to-mjcf urdf/galbot_one_golf_fixed_base.urdf \
  --output mjcf/galbot_one_golf_planar_base.xml \
  --metadata config/mjcf/metadata_planar_base.json \
  --default-metadata config/mjcf/default.json \
  --actuator-metadata config/mjcf/actuator.json \
  --appendix config/mjcf/appendix_planar_base.xml \
  --collision-type mesh
```

## Floating Base

`mjcf/galbot_one_golf_floating_base.xml` adds a MuJoCo freejoint base and does
not add base actuators.

```bash
urdf-to-mjcf urdf/galbot_one_golf_fixed_base.urdf \
  --output mjcf/galbot_one_golf_floating_base.xml \
  --metadata config/mjcf/metadata_floating_base.json \
  --default-metadata config/mjcf/default.json \
  --actuator-metadata config/mjcf/actuator.json \
  --appendix config/mjcf/appendix.xml \
  --collision-type mesh
```

## Collision Only

`mjcf/galbot_one_golf_collision_only.xml` keeps collision geometry only. Use it
when visual meshes are unnecessary.

```bash
urdf-to-mjcf urdf/galbot_one_golf.urdf \
  --output mjcf/galbot_one_golf_collision_only.xml \
  --metadata config/mjcf/metadata_wheeled.json \
  --default-metadata config/mjcf/default.json config/mjcf/default_wheeled.json \
  --actuator-metadata config/mjcf/actuator.json config/mjcf/actuator_wheeled.json \
  --appendix config/mjcf/appendix.xml \
  --collision-type mesh \
  --collision-only
```
