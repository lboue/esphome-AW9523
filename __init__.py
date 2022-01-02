import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import i2c
from esphome.const import (
    CONF_ID,
    CONF_INPUT,
    CONF_NUMBER,
    CONF_MODE,
    CONF_INVERTED,
    CONF_OUTPUT,
    CONF_PULLUP,
)

#AUTO_LOAD = ["mcp23x08_base"]
CODEOWNERS = ["@jenscski"]

CONF_AW9523 = "aw9523"
CONF_AW9523_ID = "aw9523_id"

DEPENDENCIES = ["i2c"]
MULTI_CONF = True

aw9523_ns = cg.esphome_ns.namespace("aw9523")

AW9523Component = aw9523_ns.class_("AW9523Component", cg.Component, i2c.I2CDevice)
AW9523GPIOPin = aw9523_ns.class_("AW9523GPIOPin", cg.GPIOPin)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.declare_id(AW9523Component),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(i2c.i2c_device_schema(0x58))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)
    return var

AW9523_PIN_SCHEMA = cv.All(
    {
        cv.GenerateID(): cv.declare_id(AW9523GPIOPin),
        cv.Required(CONF_AW9523_ID): cv.use_id(AW9523Component),
        cv.Required(CONF_NUMBER): cv.int_range(min=0, max=15),
        cv.Optional(CONF_MODE, default={}): cv.All(
            {
                cv.Optional(CONF_INPUT, default=False): cv.boolean,
                cv.Optional(CONF_PULLUP, default=False): cv.boolean,
                cv.Optional(CONF_OUTPUT, default=False): cv.boolean,
            },
#            validate_mode,
        ),
        cv.Optional(CONF_INVERTED, default=False): cv.boolean,
    }
)

@pins.PIN_SCHEMA_REGISTRY.register(CONF_AW9523_ID, AW9523_PIN_SCHEMA)
async def sx1509_pin_to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    parent = await cg.get_variable(config[CONF_AW9523_ID])
    cg.add(var.set_parent(parent))

    num = config[CONF_NUMBER]
    cg.add(var.set_pin(num))
    cg.add(var.set_inverted(config[CONF_INVERTED]))
    cg.add(var.set_flags(pins.gpio_flags_expr(config[CONF_MODE])))
    return var