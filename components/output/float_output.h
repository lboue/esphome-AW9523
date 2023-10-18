 #pragma once
 
 #include "esphome/core/component.h"
 #include "binary_output.h"
 
 namespace esphome {
 namespace output {
 
 #define LOG_FLOAT_OUTPUT(this) \
   LOG_BINARY_OUTPUT(this) \
   if (this->max_power_ != 1.0f) { \
     ESP_LOGCONFIG(TAG, "  Max Power: %.1f%%", this->max_power_ * 100.0f); \
   } \
   if (this->min_power_ != 0.0f) { \
     ESP_LOGCONFIG(TAG, "  Min Power: %.1f%%", this->min_power_ * 100.0f); \
   }
 
 class FloatOutput : public BinaryOutput {
  public:
   void set_max_power(float max_power);
 
   void set_min_power(float min_power);
 
   void set_zero_means_zero(bool zero_means_zero);
 
   void set_level(float state);
 
   virtual void update_frequency(float frequency) {}
 
   // ========== INTERNAL METHODS ==========
   // (In most use cases you won't need these)
 
   float get_max_power() const;
 
   float get_min_power() const;
 
  protected:
   void write_state(bool state) override;
   virtual void write_state(float state) = 0;
 
   float max_power_{1.0f};
   float min_power_{0.0f};
   bool zero_means_zero_;
 };
 
 }  // namespace output
 }  // namespace esphome
