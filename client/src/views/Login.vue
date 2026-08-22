<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store";
import Layout from "@/components/layout/Layout.vue";
import PixelButton from "@/components/ui/PixelButton.vue";

const router = useRouter();
const authStore = useAuthStore();

const account = ref("");
const password = ref("");
const errorMsg = ref("");

async function handleLogin() {
  errorMsg.value = "";
  if (!account.value || !password.value) {
    errorMsg.value = "请输入账号和密码";
    return;
  }
  try {
    const user = await authStore.login(account.value, password.value);
    // 只有 admin/editor 能进管理后台
    if (user.role === "viewer") {
      errorMsg.value = "当前账号为访客角色，无管理权限";
      return;
    }
    router.push("/admin");
  } catch (e: any) {
    errorMsg.value = e.message || "登录失败";
  }
}
</script>

<template>
    <Layout>
        <section class="py-16">
            <div class="max-w-md mx-auto px-4">
                <div
                    class="bg-white border-4 border-black rounded-xl p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]"
                >
                    <div class="text-center mb-8">
                        <div class="text-5xl mb-3">🔐</div>
                        <h1 class="pixel-text text-2xl">登录</h1>
                        <p class="text-sm text-gray-500 mt-2">
                            管理后台需要管理员或编辑者角色
                        </p>
                    </div>

                    <form class="space-y-5" @submit.prevent="handleLogin">
                        <div>
                            <label class="block mb-2 pixel-text text-sm">
                                用户名 / 邮箱
                            </label>
                            <input
                                v-model="account"
                                type="text"
                                placeholder="请输入用户名或邮箱"
                                class="w-full p-3 border-4 border-black focus:outline-none focus:ring-2 focus:ring-sky"
                            />
                        </div>

                        <div>
                            <label class="block mb-2 pixel-text text-sm">
                                密码
                            </label>
                            <input
                                v-model="password"
                                type="password"
                                placeholder="请输入密码"
                                class="w-full p-3 border-4 border-black focus:outline-none focus:ring-2 focus:ring-sky"
                            />
                        </div>

                        <div
                            v-if="errorMsg"
                            class="text-red-500 pixel-text text-sm bg-red-50 border-2 border-red-300 p-3"
                        >
                            {{ errorMsg }}
                        </div>

                        <PixelButton
                            class="w-full !justify-center"
                            type="submit"
                            :loading="authStore.loading"
                        >
                            <span class="w-full text-center">🚀 登录</span>
                        </PixelButton>
                    </form>

                    <div class="mt-6 text-center text-sm">
                        没有账号？
                        <router-link to="/register" class="text-sky-700 font-bold">
                            注册一个
                        </router-link>
                    </div>
                </div>
            </div>
        </section>
    </Layout>
</template>
